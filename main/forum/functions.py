import magic
from django.core.exceptions import ValidationError
from notification.models import Notification
from django.utils import timezone


def validate_image_or_video(value):
    # Определяем MIME-тип файла
    file_mime_type = magic.from_buffer(value.read(), mime=True)
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/avi', 'video/mov']

    # Сбрасываем указатель в начале файла после чтения
    value.seek(0)

    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file format. Please upload an image or video.')

def change_notif(obj):

    obj_verbose_name = obj._meta.verbose_name

    if obj_verbose_name == 'Post':
        notif = obj.notifications.filter(type='p_like').first()
        if notif:
            notif.description = f'Ваш пост "{obj.title[:10]}..." собрал {obj.likes} лайка(ов)'
            notif.event_date = timezone.now()
        else:
            Notification.objects.create(
                user=obj.user,
                description=f'Ваш пост "{obj.title[:10]}..." собрал {obj.likes} лайка(ов)',
                post=obj,
                event_date=timezone.now(),
                type='p_like'
            )
    else:
        notif = obj.notifications.filter(type='c_like').first()
        if notif:
            notif.description = f'Ваш комментарий "{obj.text[:10]}..." собрал {obj.likes} лайка(ов)'
            notif.event_date = timezone.now()
        else:
            Notification.objects.create(
                user=obj.user,
                description=f'Ваш комментарий "{obj.text[:10]}..." собрал {obj.likes} лайка(ов)',
                post=obj.post,
                comment=obj,
                event_date=timezone.now(),
                type='c_like'
            )