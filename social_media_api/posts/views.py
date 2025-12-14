from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Optionally, allow filtering by title/content
        queryset = Post.objects.all()
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # Allow filtering comments by post ID
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all the users the authenticated user is following
        following_users = request.user.following.all()
        
        # Add the authenticated user to their own feed if necessary
        # (so they see their own posts in the feed)
        following_users = following_users | request.user
        
        # Get posts from users that the current user follows
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Serialize the posts
        serializer = PostSerializer(posts, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)


# posts/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Post, Like
from .serializers import PostSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

@api_view(['POST'])
def like_post(request, pk):
    """Like a post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Prevent a user from liking the post multiple times
    if Like.objects.filter(post=post, user=request.user).exists():
        return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    # Create the like
    like = Like.objects.create(post=post, user=request.user)

    # Create a notification for the post owner
    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb="liked your post",
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=post.id
    )

    return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def unlike_post(request, pk):
    """Unlike a post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Ensure the user has liked the post before attempting to unlike
    like = get_object_or_404(Like, post=post, user=request.user)
    like.delete()

    # Create a notification for the post owner about unliking
    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb="unliked your post",
        target_content_type=ContentType.objects.get_for_model(post),
        target_object_id=post.id
    )

    return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)
