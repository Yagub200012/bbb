from django.shortcuts import render, redirect
from .models import User
from .functions import access
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from forum.models import Post


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

def sign_up(request):
    access_token = request.COOKIES.get('accessToken', None)
    if access_token:
        if access(access_token):
            return redirect('profile')
        refresh_token = request.COOKIES.get('refreshToken', None)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = HttpResponseRedirect(reverse('profile'))  # Заменить на нужный URL
            response.set_cookie('accessToken', access_token, httponly=True, secure=True)
            return response
        except TokenError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return render(request, 'sign_up.html')


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
                'mark':user_inst.mark,
                'posts':[]
            }
            posts = (Post.objects
                     .filter(user = user_inst)
                     .order_by('-created_at')
                     .prefetch_related('subsector'))
            for post in posts:
                user['posts'].append({
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'created_at': post.created_at,
                    'likes': post.likes,
                    'dislikes': post.dislikes,
                    'language': post.language,
                    'user': post.user.username,
                    'user_image': post.user.photo,
                    'user_mark': post.user.mark,

                    'subsector_title': post.subsector.title,
                    'subsector_id': post.subsector.id,
                    'sector_id': post.subsector.sector,
                })
            return render(request, 'profile.html', {'user': user})

    # Если токен недействителен или отсутствует
    return redirect('login_rend')