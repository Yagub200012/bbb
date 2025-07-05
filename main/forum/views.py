from django.shortcuts import render, redirect
from authorization.functions import access
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from authorization.models import AuthorUser
from notification.models import Notification
from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import *
from django.views.decorators.http import require_http_methods
from .functions import change_notif


@require_http_methods(["GET"])  # DONE
def main_page(request):
    access_token = request.COOKIES.get('accessToken', None)

    have_notification = False
    user = False
    if access_token:
        user = access(access_token)
        have_notification = Notification.objects.filter(
            user=user,
            checked=False
        ).exists()

    sectors_data = Sector.objects.prefetch_related('subsectors')
    sectors = []
    sec_id = 0
    for sector in sectors_data:
        sectors.append({
            'id': sector.id,
            'title': sector.title,
            'color': sector.color,
            'image': sector.image,
            'logo': sector.logo,
            'subsectors': []
        })
        for subsector in sector.subsectors.all():
            sectors[sec_id]['subsectors'].append({
                'id': subsector.id,
                'title': subsector.title,
            })
        sec_id += 1
    posts = (Post.objects
             .all()
             .order_by('-created_at')
             .select_related(
        'subsector',
        'user',
    ).prefetch_related(
        'images',
        Prefetch(
            'reaction_set',
            queryset=Reaction.objects.filter(user=user),
            to_attr='user_reactions'
        )
    )[:10])
    context = {
        'sectors': sectors,
        'posts': posts,
        'have_notification': have_notification,
        'user_id': user.id if user else 1,
    }
    return render(request, 'main.html', context)


@require_http_methods(["GET"])  # DONE
def sector(request, pk):
    access_token = request.COOKIES.get('accessToken', None)

    have_notification = False
    user = False
    if access_token:
        user = access(access_token)
        have_notification = Notification.objects.filter(
            user=user,
            checked=False
        )

    sec = Sector.objects.filter(id=pk).prefetch_related('subsectors').first()
    sect = {
        'id': pk,
        'title': sec.title,
        'subsectors': []
    }
    subsector = sec.subsectors.filter(sector=pk).first()
    sect['subsectors'].append({
        'id': subsector.id,
        'title': subsector.title,
    })
    posts = (Post.objects.filter(subsector__sector=pk)
             .order_by('-created_at')
             .select_related(
        'subsector',
        'user',
    ).prefetch_related(
        'images',
        Prefetch(
            'reaction_set',
            queryset=Reaction.objects.filter(user=user),
            to_attr='user_reactions'
        )
    )[:10])

    context = {
        'sector': sect,
        'posts': posts,
        'have_notification': have_notification,
        'user_id': user.id if user else 1,
    }
    return render(request, 'sector.html', context)


@require_http_methods(["GET"])  # DONE
def subsector_post(request):
    access_token = request.COOKIES.get('accessToken', None)

    have_notification = False
    user = False
    if access_token:
        user = access(access_token)
        have_notification = Notification.objects.filter(
            user=user,
            checked=False
        )

    subsector_id = request.GET.get('subsector_id', None)
    if not subsector_id:
        return render(request, '404page.html')
    posts = (Post.objects
             .filter(subsector=subsector_id)
             .order_by('-created_at')
             .select_related(
        'subsector',
        'user',
    ).prefetch_related(
        'images',
        Prefetch(
            'reaction_set',
            queryset=Reaction.objects.filter(user=user),
            to_attr='user_reactions'
        )
    )[:10])

    first_post = posts.first()
    if not first_post:
        return render(request, '404page.html')
    subsector = {
        'id': subsector_id,
        'title': first_post.subsector.title,
        'description': first_post.subsector.description,
        'sector_title': first_post.subsector.sector,
    }

    return render(request, 'subsector.html', {
        'subsector': subsector,
        'have_notification': have_notification,
        'user_id': user.id if user else 1,
        'posts': posts,
    })


def post_create(request):
    access_token = request.COOKIES.get('accessToken', None)

    have_notification = False
    user = False
    if access_token:
        user = access(access_token)
        have_notification = Notification.objects.filter(
            user=user,
            checked=False
        )

    access_token = request.COOKIES.get('accessToken', None)
    if access_token:
        sectors_data = Sector.objects.prefetch_related('subsectors')
        sectors = []
        sec_id = 0

        for sector in sectors_data:
            sectors.append({
                'id': sector.id,
                'title': sector.title,
                'subsectors': []
            })
            for subsector in sector.subsectors.all():
                sectors[sec_id]['subsectors'].append({
                    'id': subsector.id,
                    'title': subsector.title,
                })
            sec_id += 1
        if access(access_token):
            return render(request, 'post_form.html', {
                'sectors': sectors,
                'have_notification': have_notification,
                'user_id': user.id if user else 1,
            })
        refresh_token = request.COOKIES.get('refreshToken', None)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = HttpResponseRedirect(reverse('profile'))
            response.set_cookie('accessToken', access_token, httponly=True, secure=True)
            return response
        except TokenError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return redirect('login_rend')


@require_http_methods(["GET"])
def retrieve_post(request, pk):
    access_token = request.COOKIES.get('accessToken', None)

    have_notification = False
    user = None
    if access_token:
        user = access(access_token)
        have_notification = Notification.objects.filter(
            user=user,
            checked=False
        )

    post = Post.objects.filter(id=pk).values(
        'id',
        'title',
        'content',
        'created_at',
        'subsector',
        'likes',
        'dislikes',
        'language',
        "subsector__title",
        "subsector__sector__title",
        'anonymously',
        'user__id',
        'user__username',
        'user__avatar',
        'user__mark',

    ).first()
    if post:
        react_type = Reaction.objects.filter(post=pk, user=user).values('type').first()
        if react_type:
            post['react_type'] = react_type['type']

        images = Image.objects.filter(post = pk)

        comments_db = Comment.objects.filter(post=post['id']).select_related(
            'user', 'replied_to'
        ).prefetch_related(
            Prefetch(
                'reaction_set',
                queryset=Reaction.objects.filter(user=user),
                to_attr='user_reactions'
            )
        )[:15]

        post['comments'] = comments_db
        return render(request, 'post.html', {
            'post': post,
            'have_notification': have_notification,
            'user_id': user.id if user else 1,
            'images':images,
        })
    else:
        return render(request, '404page.html')


def post_edit(request, pk):
    access_token = request.COOKIES.get('accessToken', None)

    if access_token:
        sectors_data = Sector.objects.prefetch_related('subsectors')
        user = request.user

        post = Post.objects.filter(id=pk).values(
            'content',
            'title',
            'user__id'
        ).first()
        if not user.pk == post['user__id']:
            return
        sectors = []
        sec_id = 0
        for sector in sectors_data:
            sectors.append({
                'id': sector.id,
                'title': sector.title,
                'subsectors': []
            })
            for subsector in sector.subsectors.all():
                sectors[sec_id]['subsectors'].append({
                    'id': subsector.id,
                    'title': subsector.title,
                })
            sec_id += 1
        if access(access_token):
            return render(request, 'post_form.html', {'sectors': sectors})
        refresh_token = request.COOKIES.get('refreshToken', None)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = HttpResponseRedirect(reverse('profile'))
            response.set_cookie('accessToken', access_token, httponly=True, secure=True)
            return response
        except TokenError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return redirect('login_rend')  # badger.633647


class ReactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post')
        comment_id = request.data.get('comment')
        type = request.data.get('type')
        user = request.user

        if not (post_id or comment_id):
            return Response({'error': 'Invalid request'}, status=400)

        if post_id:
            obj = Post.objects.filter(id=post_id).prefetch_related('notifications').first()
            react, created = Reaction.objects.get_or_create(user=user, post=obj)
        else:
            obj = Comment.objects.filter(id=comment_id).prefetch_related('notifications').first()
            react, created = Reaction.objects.get_or_create(user=user, comment=obj)

        if created:
            with transaction.atomic():
                react.type = type
                if type == 'like':
                    obj.likes += 1
                    change_notif(obj)
                else:
                    obj.dislikes += 1
                obj.save()
                react.save()
                return Response({}, status=200)

        if react.type == 'nothing':
            with transaction.atomic():
                react.type = type
                if type == 'like':
                    obj.likes += 1
                    change_notif(obj)
                else:
                    obj.dislikes += 1
                react.save()
                obj.save()
            return Response({}, status=200)
        elif react.type == 'like':
            with transaction.atomic():
                obj.likes -= 1
                change_notif(obj)
                if type == 'like':
                    react.type = 'nothing'
                else:
                    obj.dislikes += 1
                    react.type = type
                obj.save()
                react.save()
            return Response({}, status=200)
        else:
            with transaction.atomic():
                obj.dislikes -= 1
                if type == 'dislike':
                    react.type = 'nothing'
                else:
                    obj.likes += 1
                    change_notif(obj)
                    react.type = type
                obj.save()
                react.save()
            return Response({}, status=200)
