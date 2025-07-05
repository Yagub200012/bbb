from rest_framework import serializers
from ..models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            'type',
            'description',
            'event_date',
            'post'
        ]