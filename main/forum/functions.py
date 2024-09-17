import magic
from django.core.exceptions import ValidationError


def validate_image_or_video(value):
    # Определяем MIME-тип файла
    file_mime_type = magic.from_buffer(value.read(), mime=True)
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/avi', 'video/mov']

    # Сбрасываем указатель в начале файла после чтения
    value.seek(0)

    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file format. Please upload an image or video.')
