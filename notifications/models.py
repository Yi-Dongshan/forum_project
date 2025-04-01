# notifications/models.py
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post, Comment
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('comment', '评论'),
        ('reply', '回复'),
        ('like', '点赞'),
        ('mention', '提及'),
        ('system', '系统通知'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    text = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.recipient.username}的{self.get_notification_type_display()}'

    def mark_as_read(self):
        self.is_read = True
        self.save()

@receiver(post_save, sender=Notification)
def notification_post_save(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.recipient.id}_notifications',
            {
                'type': 'notification_message',
                'count': Notification.objects.filter(recipient=instance.recipient, is_read=False).count()
            }
        )
