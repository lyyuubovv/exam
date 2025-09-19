from django.conf import settings
from django.core.cache import cache
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import requests

from .models import Article
from .serializers import ArticleSerializer

class UpdateArticlesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cache_key = 'articles_update_lock'
        if cache.get(cache_key):
            return Response({'detail': 'Recently updated. Wait 30 minutes.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        api_key = getattr(settings, 'NEWSAPI_KEY', '') or request.data.get('api_key')
        if not api_key:
            return Response({'detail': 'NEWSAPI_KEY not configured. Provide NEWSAPI_KEY in settings or pass api_key in POST body.'}, status=status.HTTP_400_BAD_REQUEST)

        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
        except Exception as e:
            return Response({'detail': f'Error fetching from NewsAPI: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)

        data = r.json()
        saved = 0
        for item in data.get('articles', []):
            # Parse published date
            published = parse_datetime(item.get('publishedAt')) if item.get('publishedAt') else None
            defaults = {
                'source_id': item.get('source', {}).get('id'),
                'source_name': item.get('source', {}).get('name'),
                'author': item.get('author'),
                'title': item.get('title'),
                'description': item.get('description'),
                'url_to_image': item.get('urlToImage'),
                'published_at': published or timezone.now(),
                'content': item.get('content'),
            }
            obj, created = Article.objects.get_or_create(url=item.get('url'), defaults=defaults)
            if created:
                saved += 1

        cache.set(cache_key, True, timeout=60*30)
        return Response({'saved': saved})

class ListArticlesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # cache by query params
        cache_key = f'articles_list:{request.GET.urlencode()}'
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        qs = Article.objects.all().order_by('-published_at')
        if request.GET.get('fresh') == 'true':
            qs = qs.filter(published_at__gte=timezone.now() - timedelta(days=1))
        title_contains = request.GET.get('title_contains')
        if title_contains:
            qs = qs.filter(title__icontains=title_contains)

        serializer = ArticleSerializer(qs, many=True)
        cache.set(cache_key, serializer.data, timeout=60*10)
        return Response(serializer.data)
