from django.contrib import admin
from .models import User

@admin.register(User)
class SectorAdmin(admin.ModelAdmin):
    list_display = (
        'photo',
        'username',
        'emoji',
        'bio',
        'email',
        'email_verified',
        'is_staff',
        'created_at',
        'password'
    )

