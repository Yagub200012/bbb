from email.policy import default

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Q

class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(("User must have an username"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # photo = models.FileField(upload_to='user_photos/', null=True)
    avatar = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=40, unique=True)
    emoji = models.CharField(max_length=5, null=True, blank=True)
    bio = models.TextField(max_length=2000, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=120, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    word_dict = models.JSONField(default=dict, null=False)
    # is_banned = models.BooleanField(default=False)

    GD = '#dbbb2c'
    SL = '#7a7a7a'
    BR = '#db812c'
    RD = '#eb4444'
    BL = '#1b7cde'
    PR = '#bd1bde'
    GR = '#058585'

    MARKS = (
        (GD, 'gold'),
        (SL, 'silver'),
        (BR, 'bronze'),
        (RD, 'red'),
        (BL, 'blue'),
        (PR, 'purple'),
        (GR, 'green'),
    )

    mark = models.CharField(max_length=20, choices=MARKS, null=True, blank=True)


    # Указание уникальных имен для обратных связей
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set', blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "User"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True




class Subscription(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='subscriber')
    subscriber = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='subscribed')

    class Meta:
        unique_together = ('user', 'subscriber')
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        





class AuthorUser(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='user')
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='author')

    class Meta:
        unique_together = ('user','author')
        constraints = [
            models.CheckConstraint(
                check=~Q(author=models.F("user")),
                name="user_not_equal_author",
            )
        ]