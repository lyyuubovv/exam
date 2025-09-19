from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, ActivateSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ActivateView(generics.GenericAPIView):
    serializer_class = ActivateSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        try:
            user = User.objects.get(email=email, activation_code=code)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or code'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.activation_code = None
        user.save()
        return Response({'status': 'activated'})
