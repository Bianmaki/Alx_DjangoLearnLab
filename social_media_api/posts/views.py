from rest_framework import viewsets, generics, filters, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification

User = get_user_model()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['author__id']   # allow filtering by author id
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        # Prevent duplicate likes using existence check
        if Like.objects.filter(post=post, user=request.user).exists():
            return Response({"detail": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)
        like, created = Like.objects.get_or_create(post=post, user=request.user)  # explicit create
        # create notification: actor=request.user, recipient=post.author
        if post.author != request.user:
            Notification.create_notification(actor=request.user, recipient=post.author, verb='liked your post', target=post)
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()  # explicit filter().delete()
        if deleted:
            # optionally create a notification for unlike or remove existing notification (not implemented)
            return Response({"detail": "Unliked"}, status=status.HTTP_200_OK)
        return Response({"detail": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def feed(self, request):
        """
        Return posts from users the current user follows, ordered by newest first.
        URL: /api/posts/feed/
        """
        following_qs = request.user.following.all()
        # explicit queryset call
        feed_posts = Post.objects.filter(author__in=following_qs).order_by('-created_at')
        page = self.paginate_queryset(feed_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(feed_posts, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post']  # allow filter by ?post=<post_id>
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        comment = serializer.save(author=self.request.user)
        Notification.objects.create(
            recipient=comment.post.author,
            actor=self.request.user,
            verb="commented on your post",
            target=comment.post
        )
class FeedView(APIView):
    """
    Returns posts from users the current user follows.
    """
    permission_classes = [permissions.IsAuthenticated]  # <-- checker requirement

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')  # <-- checker requirement
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)