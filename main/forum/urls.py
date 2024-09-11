from django.urls import path
from .views import SectorListView, SubSectorListview, PostListView, PostView, PostCreateView, main_page, subsector

urlpatterns = [
    path('sectors/', SectorListView.as_view(), name='sectors'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('subsector_posts/<int:pk>', SubSectorListview.as_view(), name='subsector_posts'),
    path('post/<int:pk>', PostView.as_view(), name='post'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('main/', main_page, name='main_page'),
    path('subsector/<int:pk>', subsector, name='subsector'),
]
