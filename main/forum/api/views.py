from rest_framework.permissions import IsAuthenticated
from ..models import *
from .serializers import SectorSerializer, SubSectorPostSerializer, PostSerializer, CommentSerializer
from rest_framework import generics, status
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse


class SectorListView(generics.ListAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAdminOrReadOnly]


class SubSectorListview(generics.RetrieveAPIView):
    queryset = SubSector.objects.all()
    serializer_class = SubSectorPostSerializer
    permission_classes = [IsAdminOrReadOnly]


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PostView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class LoadMorePostsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))
        subsector = int(request.GET.get('subsector',0))
        sector = int(request.GET.get('sector',0))
        if subsector:
            posts = Post.objects.filter(subsector=subsector).order_by('-created_at')[offset:offset + limit]
        elif sector:
            posts = Post.objects.filter(subsector__sector=sector).order_by('-created_at')[offset:offset + limit]
        else:
            posts = Post.objects.all().order_by('-created_at')[offset:offset + limit]
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoadMoreCommentsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 15))
        post = int(request.GET['post'])
        comments = Comment.objects.filter(post = post)[offset:offset + limit]
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# class LoadMoreCommentsView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def get(self, request, post_id):
#         from_id = int(request.GET.get('from_id', 0))
#         direction = request.GET.get('direction', 'down')
#         limit = 20
#
#         if direction == 'down':
#             qs = Comment.objects.filter(post_id=post_id, id__gt=from_id).order_by('id')[:limit]
#         else:
#             qs = Comment.objects.filter(post_id=post_id, id__lt=from_id).order_by('-id')[:limit]
#
#         comments = CommentSerializer(qs, many=True).data
#         if direction == 'up':
#             comments = list(reversed(comments))
#
#         return Response({'comments': comments})
#
# def get_last_comment_id(request, post_id):
#     last = Comment.objects.filter(post_id=post_id).order_by('-id').first()
#     return JsonResponse({'last_id': last.id if last else 0})
