from .serializers import RegisterSerializer, UserSerializer, SubscriptionSerializer
from rest_framework import generics
from ..models import User, Subscription
from rest_framework.permissions import AllowAny
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsOwnerOrReadOnly]
    permission_classes = [AllowAny]

class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

class SubscriptionDeleteView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, pk):
        obj = Subscription.objects.filter(user=pk, subscriber=request.user.id).first()
        if obj:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

