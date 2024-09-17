from django.contrib import admin
from .models import Sector, SubSector, Post, Comment, Media


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(SubSector)
class SubSectorAdmin(admin.ModelAdmin):
    list_display = ('title', 'sector')
    search_fields = ('title',)
    list_filter = ('sector',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'subsector', 'anonymously', 'created_at', 'likes', 'user')
    search_fields = ('title', 'content')
    list_filter = ('user', 'subsector', 'created_at')

    def save_model(self, request, obj, form, change):
        if not change:  # Если это новый объект
            obj.user = request.user  # Устанавливаем текущего пользователя
        super().save_model(request, obj, form, change)



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'likes')
    search_fields = ('text',)
    list_filter = ('user', 'post', 'created_at')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('comment', 'media')
    search_fields = ('comment',)
    list_filter = ('comment',)
