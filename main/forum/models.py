from django.db import models
from django.db.models import Q
from authorization.models import User
from .functions import validate_image_or_video


class Sector(models.Model):
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='sectors/', null=True, blank=True)
    logo = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"

    def __str__(self):
        return self.title


class SubSector(models.Model):
    sector = models.ForeignKey(Sector, related_name='subsectors', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=3000, null=True, blank=True)

    class Meta:
        verbose_name = "Subsector"
        verbose_name_plural = "Subsectors"

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=5000, null=True, blank=True, )
    content_censored = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    LANG = (
        ('RU', 'russian'),
        ('EN', 'english'),
        ('AZ', 'azerbaijani'),
    )

    language = models.CharField(max_length=20, choices=LANG, default='EN')

    subsector = models.ForeignKey(SubSector, related_name='posts', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymously = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    image_link = models.CharField(max_length=255, null=False)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Comment(models.Model):
    text = models.TextField(max_length=5000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', blank=True, null=True, )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    comment = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subcomments')
    replied_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='replies')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = "Comments"


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=10, default='nothing', null=False, choices=[
        ('like', 'лайк'),
        ('dislike', 'дизлайк'),
        ('nothing', 'ничего')
    ])
