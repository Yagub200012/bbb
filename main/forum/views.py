from pydoc import describe

from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializers import SectorSerializer, SubSectorPostSerializer, PostSerializer
from rest_framework import generics, status
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from django.views.decorators.http import require_http_methods


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

    # TEMPLATES  RENDERING


@require_http_methods(["GET"])
def main_page(request):
    sectors_data = Sector.objects.prefetch_related('subsectors')
    sectors = []
    sec_id = 0
    for sector in sectors_data:
        sectors.append({
            'id': sector.id,
            'title': sector.title,
            'subsectors': []
        })
        for subsector in sector.subsectors.all():
            sectors[sec_id]['subsectors'].append({
                'id': subsector.id,
                'title': subsector.title,
                # 'description':subsector.description
            })
        sec_id += 1
        print(sectors)
    return render(request, 'main.html', {'sectors': sectors})


@require_http_methods(["GET"])
def subsector(request, pk):
    # Получаем объект SubSector с указанным ID, делаем select_related и prefetch_related для оптимизации запросов
    subsector_posts = (SubSector.objects
                       .select_related('sector')  # Подгружаем связанную модель Sector одним запросом
                       .prefetch_related('posts')  # Подгружаем связанные Post для SubSector
                       .filter(id=pk)  # Фильтруем по id
                       .first())  # Берём первый объект (в данном случае, единственный)

    # Проверяем, что subsector_posts не None (в случае если объект не найден)
    if not subsector_posts:
        return get_object_or_404(SubSector, id=pk)  # Возвращаем 404, если SubSector не найден

    # Формируем словарь с данными для передачи в шаблон
    subsector = {
        'id': pk,
        'title': subsector_posts.title,
        'description': subsector_posts.description,  # Исправлено 'describtion' на 'description'
        'sector': {
            'id': subsector_posts.sector.id,
            'title': subsector_posts.sector.title
        },
        'posts': []
    }

    # Используем prefetch_related для оптимизации запросов
    for post in subsector_posts.posts.all():
        subsector['posts'].append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'likes': post.likes,
            'dislikes': post.dislikes,
            'language': post.language,
            'user': post.user.username,  # Если нужно имя пользователя, иначе можно просто пост.user
        })

    # Печатаем для отладки (по необходимости)
    print(subsector)
    return render(request, 'subsector.html', {'subsector': subsector})

