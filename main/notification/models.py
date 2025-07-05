from authorization.models import User
# from forum.models import Post, Comment
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    description = models.CharField(null=False, max_length=100)
    link = models.CharField(null=False, max_length=100)
    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    comment = models.ForeignKey('forum.Comment', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    checked = models.BooleanField(default=False)
    event_date = models.DateTimeField(null=True)
    type = models.CharField(choices=[
        ('reply','reply'),
        ('comment','comment'),
        ('p_like','like on post'),
        ('c_like','like on comment')
    ], null=True, blank=True, max_length=10)