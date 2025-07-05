from django.urls import path, include
from .views import (SectorListView, SubSectorListview, PostListView, PostView, PostCreateView, CommentCreateView, LoadMorePostsView, LoadMoreCommentsView)
                    # LoadMoreCommentsView, get_last_comment_id)

urlpatterns = [
    path('sectors/', SectorListView.as_view(), name='sectors'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('subsector_posts/<int:pk>', SubSectorListview.as_view(), name='subsector_posts'),
    path('post/<int:pk>', PostView.as_view(), name='post'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('comment_create/', CommentCreateView.as_view(), name='comment_create'),
    path('load-posts/', LoadMorePostsView.as_view(), name='load-posts'),
    path('load-comments/', LoadMoreCommentsView.as_view(), name='load-comments'),
    # path('get_last_comment_id/<int:post_id>', get_last_comment_id, name='get_last_comment_id')
]
