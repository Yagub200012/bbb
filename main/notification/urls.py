from django.urls import path, include
from .views import notif

urlpatterns = [
    path('', notif, name='notif'),
    path('api/', include('notification.api.urls')),
]

