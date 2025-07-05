from django.shortcuts import render
from authorization.functions import access
from .models import *
from django.db import connection


def notif(request):
    access_token = request.COOKIES.get('accessToken', None)

    if access_token:
        user_inst = access(access_token)
        if user_inst:
            notifications = Notification.objects.filter(user=user_inst).order_by('-event_date')[:15]
            # Сохраняем в контекст НЕизменённые данные
            context = {'notifications': list(notifications.iterator())}

            # # Меняем и обновляем
            # for notification in notifications:
            #     notification.checked = True
            # Notification.objects.bulk_update(notifications, ['checked'])

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE notification_notification SET checked = %s WHERE checked = %s",
                    [True, False]
                )

            return render(request, 'notifications.html', context)
        else:
            return render(request, '404page.html')
    else:
        return render(request, 'login.html')