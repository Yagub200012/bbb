from django.urls import path, include
from .views import main_page, subsector_post

urlpatterns = [
    path('main/', main_page, name='main_page'),
    path('subsector_post/', subsector_post, name='subsector_post'),
    path('api/', include('forum.api.urls')),
]
