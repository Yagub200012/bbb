from django.urls import path, include
from .views import login_rend, profile, logout, sign_up, edit_prof

urlpatterns = [
    # path('main/', main_page, name='main_page'),
    path('api/', include('authorization.api.urls')),
    path('sign_up/', sign_up, name= 'sign_up_rend'),
    path('login/', login_rend, name= 'login_rend'),
    path('logout/', logout,  name= 'logout'),
    path('profile/<int:pk>', profile, name= 'profile'),
    path('edit_profile/<int:pk>', edit_prof, name='edit_prof'),
]
