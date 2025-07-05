from celery import shared_task
import requests
from django.conf import settings
from .models import Image, Post
from PIL import Image as im
from io import BytesIO

@shared_task()
def upload_image(image, post_id:int):
    headers = {"Authorization": f"Client-ID {settings.IMGUR_CLIENT_ID}"}
    img = im.open(BytesIO(image))

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    resp = requests.post(
        "https://api.imgur.com/3/image",
        files={'image': img_byte_arr},
        headers=headers,
        timeout=10
    )
    Image.objects.create(post=Post.objects.get(id=post_id), image_link = resp.json()["data"]["link"][20::])
