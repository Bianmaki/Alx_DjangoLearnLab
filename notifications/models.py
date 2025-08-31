# notifications/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=255)  # e.g., "liked", "commented on", "followed"
    # Generic relation to any target (Post, Comment, User, etc.)
    target_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    target_object_id = models.CharField(max_length=255, null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Notification({self.actor} {self.verb} -> {self.recipient})"

    @classmethod
    def create_notification(cls, actor, recipient, verb, target=None):
        """
        Convenience helper to create a notification.
        """
        target_ct = None
        target_id = None
        if target is not None:
            target_ct = ContentType.objects.get_for_model(target.__class__)
            target_id = getattr(target, 'pk', None)
        return cls.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target_content_type=target_ct,
            target_object_id=str(target_id) if target_id is not None else None
        )
