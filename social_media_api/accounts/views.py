from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer
)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Serialize incoming data for user registration
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Save the user and get the token
        token, _ = Token.objects.get_or_create(user=user)  # Token creation
        return Response({
            'token': token.key,  # Send token in response
            'user': UserProfileSerializer(user).data
        })

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Serialize login credentials
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data  # User returned after successful validation
        token, _ = Token.objects.get_or_create(user=user)  # Token creation
        return Response({'token': token.key})  # Return token for authentication

class ProfileView(APIView):
    def get(self, request):
        # Return the logged-in user's profile data
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
