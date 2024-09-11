from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..models import *
from .serializers import SectorSerializer, SubSectorPostSerializer, PostSerializer
from rest_framework import generics, status
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

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