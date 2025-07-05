from django.urls import path, include
from .views import LoadMoreNotificationsView

urlpatterns = [
    path('load_notifications/', LoadMoreNotificationsView.as_view(), name='load_notification'),
]
