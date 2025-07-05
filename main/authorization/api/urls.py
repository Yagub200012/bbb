from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import RegisterView, UserUpdateView, SubscriptionCreateView, SubscriptionDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='user_update'),
    path('subscribe/', SubscriptionCreateView.as_view(), name='subscribe'),
    path('unsubscribe/<int:pk>', SubscriptionDeleteView.as_view(), name='unsubscribe'),
]
