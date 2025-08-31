from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField(read_only=True)
    recipient_id = serializers.IntegerField(source='recipient.id', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient_id', 'actor', 'verb', 'target_content_type', 'target_object_id', 'read', 'timestamp']
        read_only_fields = ['id', 'actor', 'recipient_id', 'timestamp']
