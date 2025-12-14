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



from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CustomUser  # Import CustomUser directly

# Retrieve all users
all_users = CustomUser.objects.all()


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Use CustomUser directly instead of get_user_model()
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        
        # Prevent following oneself
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Add user to 'following' field
        request.user.following.add(user_to_follow)
        return Response({"detail": f"You are now following {user_to_follow.username}."})


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Use CustomUser directly instead of get_user_model()
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        
        # Prevent unfollowing oneself
        if user_to_unfollow == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove user from 'following' field
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."})
