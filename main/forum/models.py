from django.db import models
from authorization.models import User
from django.template.defaulttags import comment


class Sector(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"

    def __str__(self):
        return self.title


class SubSector(models.Model):
    sector = models.ForeignKey(Sector, related_name= 'subsectors', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=3000, null=True, blank=True)


    class Meta:
        verbose_name = "Subsector"
        verbose_name_plural = "Subsectors"

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    RU = 'russian'
    EN = 'english'
    AZ = 'azerbaijani'

    LANG = (
        (RU, 'russian'),
        (EN, 'english'),
        (AZ, 'azerbaijani'),
    )

    language = models.CharField(max_length=20, choices=LANG, default=EN)

    subsector = models.ForeignKey(SubSector, related_name='posts', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(max_length=5000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='sub_comments', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = "Comments"


class Media(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    media = models.FileField(upload_to='comment_files/')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'post', 'comment')

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'post', 'comment')