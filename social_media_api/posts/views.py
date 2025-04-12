from rest_framework import viewsets, permissions, filters, status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like
from .serializers import LikeSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import generics



# Custom permission to allow authors to edit/delete their own content
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]  # Enable search
    search_fields = ['title', 'content']      # Search by title or content

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Save the comment and assign the current user as the author
        comment = serializer.save(author=self.request.user)

        # Get the post that was commented on
        post = comment.post

        # Avoid sending notification to yourself
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,                      # Who gets notified
                actor=self.request.user,                    # Who did the comment
                verb='commented on your post',              # What happened
                content_type=ContentType.objects.get_for_model(post),  # Post type
                object_id=post.id                           # Post ID
            )

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()  # 🔁 Get users they are following
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # 🔍 Get the post being liked
        try:
            post = generics.get_object_or_404(Post, pk=pk)

        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=404)

        # ❤️ Like the post if not already liked
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'detail': 'Already liked this post.'}, status=400)

        # 🔔 Create a notification if not self-like
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,               # 👤 Who should get the notification
                actor=request.user,                  # 🧍‍♂️ Who performed the action
                verb='liked your post',              # 📣 Action description
                content_type=ContentType.objects.get_for_model(post),  # 📦 Content type (Post)
                object_id=post.id                    # 🆔 ID of the post liked
            )

        # ✅ Send success response
        return Response({'detail': 'Post liked successfully.'}, status=201)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({'detail': 'Post unliked successfully.'})
        except Like.DoesNotExist:
            return Response({'detail': 'You have not liked this post.'}, status=400)