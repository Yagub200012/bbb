from django.urls import path, include
from .views import main_page, subsector_post, post_create

urlpatterns = [
    path('', main_page, name='main_page'),
    path('subsector_post/', subsector_post, name='subsector_post'),
    path('api/', include('forum.api.urls')),
    path('post_create/', post_create, name= 'post_create')
]
