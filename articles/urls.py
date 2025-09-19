from django.urls import path
from .views import UpdateArticlesView, ListArticlesView

urlpatterns = [
    path('update/', UpdateArticlesView.as_view(), name='articles-update'),
    path('', ListArticlesView.as_view(), name='articles-list'),
]
