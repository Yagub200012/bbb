from django.shortcuts import render, redirect
from .models import User, Subscription
from .functions import access
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from forum.models import Post, Reaction
from notification.models import Notification
from django.db.models import Prefetch

def logout(request):
    response = HttpResponseRedirect(reverse('login_rend'))
    response.delete_cookie('accessToken')
    response.delete_cookie('refreshToken')
    return response


def login_rend(request):
    access_token = request.COOKIES.get('accessToken', None)
    if access_token:
        user = access(access_token).id if access(access_token) else None
        if user:
            return redirect('profile', pk=user)
        refresh_token = request.COOKIES.get('refreshToken', None)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = HttpResponseRedirect(reverse('profile'))  # Заменить на нужный URL
            response.set_cookie('accessToken', access_token, httponly=True, secure=True)
            return response
        except Exception as e:
            return logout(request)
    return render(request, 'login.html')



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


def profile(request,pk):
    access_token = request.COOKIES.get('accessToken', None)

    user_inst = access(access_token)
    have_notification = Notification.objects.filter(
        user= user_inst,
        checked = False
    ).exists()



    if pk == 0:
        pk = user_inst.id

    is_user = False
    if user_inst:
        if user_inst.id == pk:
            is_user = True

    posts = (Post.objects
             .filter(user=pk)
             .order_by('-created_at')
             .select_related(
        'subsector',
        'user'
    )
             .prefetch_related(
        Prefetch(
            'reaction_set',
            queryset=Reaction.objects.filter(user=user_inst.id if user_inst else False),
            to_attr='user_reactions'
        )
    )[:10])
    return render(request, 'profile.html', {
        'user':posts[0].user if posts else User.objects.filter(id=pk).first(),
        'posts':posts,
        'have_notification':have_notification,
        'is_user': is_user,
        'is_subscribed': Subscription.objects.filter(user=pk, subscriber = user_inst).exists() if not is_user else False,
        })

    # Если токен недействителен или отсутствует
    # return redirect('login_rend')


def edit_prof(request,pk):
    user = User.objects.filter(id=pk).values(
        'id',
        'username',
        'avatar',
        'bio',
    ).first()
    return render(request,'edit_profile.html',{'user':user})
