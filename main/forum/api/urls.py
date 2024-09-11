from django.urls import path, include
from .views import SectorListView, SubSectorListview, PostListView, PostView, PostCreateView

urlpatterns = [
    path('sectors/', SectorListView.as_view(), name='sectors'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('subsector_posts/<int:pk>', SubSectorListview.as_view(), name='subsector_posts'),
    path('post/<int:pk>', PostView.as_view(), name='post'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
]
