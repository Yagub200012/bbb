from celery import shared_task
import requests
from django.conf import settings
from .models import User
from PIL import Image as im
from io import BytesIO

@shared_task()
def upload_avatar(image, user_id:int):
    headers = {"Authorization": f"Client-ID {settings.IMGUR_CLIENT_ID}"}
    img = im.open(BytesIO(image))  # image - это байтовые данные изображения

    # Сохраняем изображение в байтовый поток
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')  # Сохраняем в формате PNG (или любой другой формат)
    img_byte_arr.seek(0)
    resp = requests.post(
        "https://api.imgur.com/3/image",
        files={'image': img_byte_arr},
        headers=headers,
        timeout=10,
    )
    user = User.objects.get(id=user_id)
    user.avatar = resp.json()["data"]["link"][20::]
    user.save()