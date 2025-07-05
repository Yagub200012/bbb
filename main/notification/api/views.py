from rest_framework.permissions import IsAuthenticated
from ..models import *
from .serializers import NotificationSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # permission_classes = [IsAuthenticated]

class LoadMoreNotificationsView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f'ПОЛЬЗОВАТЬЕЛЬ АВТОРИЗОВАН {self.request.user}')
        return Notification.objects.filter(user=self.request.user).order_by('-event_date')

    def get(self, request):
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))
        notifs = self.get_queryset()[offset:offset + limit]
        serializer = NotificationSerializer(notifs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
