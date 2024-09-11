from django.urls import path, include
from .views import main_page, subsector

urlpatterns = [
    path('main/', main_page, name='main_page'),
    path('subsector/<int:pk>', subsector, name='subsector'),
    path('api/', include('forum.api.urls')),
]
