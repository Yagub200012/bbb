from django.contrib import admin
from .models import User, Subscription

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'avatar',
        'username',
        'emoji',
        'bio',
        'email',
        'email_verified',
        'is_staff',
        'created_at',
        'password'
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subscriber'
    )

