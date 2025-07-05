from django.urls import path, include
from .views import main_page, subsector_post, sector, post_create, retrieve_post, post_edit, ReactionView

urlpatterns = [
    path('', main_page, name='main_page'),
    path('subsector_post/', subsector_post, name='subsector_post'),
    path('api/', include('forum.api.urls')),
    path('post_create/', post_create, name='post_create'),
    path('post_edit/<int:pk>', post_edit, name='post_edit'),
    path('post/<int:pk>', retrieve_post, name='post'),
    path('sector/<int:pk>', sector, name='sector'),
    path('reaction/', ReactionView.as_view(), name='reaction'),
]
