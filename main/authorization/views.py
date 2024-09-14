from django.shortcuts import render, redirect
from .models import User
from .functions import access
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def login_rend(request):
    access_token = request.COOKIES.get('accessToken', None)
    if access_token:
        if access(access_token):
            return redirect('profile')
        refresh_token = request.COOKIES.get('refreshToken', None)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = HttpResponseRedirect(reverse('profile'))  # Заменить на нужный URL
            response.set_cookie('accessToken', access_token, httponly=True,secure=True)
            return response
        except TokenError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return render(request, 'login.html')


def logout(request):
    response = HttpResponseRedirect(reverse('login_rend'))
    response.delete_cookie('accessToken')
    response.delete_cookie('refreshToken')
    return response


def profile(request):
    access_token = request.COOKIES.get('accessToken', None)

    if access_token:
        user_inst = access(access_token)
        if user_inst:
            user = {
                'id': user_inst.id,
                'username': user_inst.username,
                'bio': user_inst.bio,
                'photo': user_inst.photo,
            }
            return render(request, 'profile.html', {'user': user})

    # Если токен недействителен или отсутствует
    return redirect('login_rend')