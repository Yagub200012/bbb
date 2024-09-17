from django.shortcuts import render, redirect
from authorization.functions import access
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from .models import *
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def main_page(request):
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
    posts_data = (Post.objects
                  .all()
                  .order_by('-created_at')
                  .prefetch_related('subsector', 'user'))
    posts = []
    post_id = 0
    for post in posts_data:
        posts.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'likes': post.likes,
            'dislikes': post.dislikes,
            'language': post.language,
            'media': [
                post.file1,
                post.file2,
                post.file3,
                post.file4,
                post.file5,
                post.file6,
            ],

            'subsector_title': post.subsector.title,
            'subsector_id': post.subsector.id,
            'sector_id': post.subsector.sector,
        })
        if post.anonymously:
            posts[post_id]['user'] = 'Anonymous'
            posts[post_id]['user_image'] = 'user_photos/anon.PNG'
            posts[post_id]['mark'] = None
        else:
            posts[post_id]['user'] = post.user.username
            posts[post_id]['user_image'] = post.user.photo
            posts[post_id]['mark'] = post.user.mark

        post_id +=1

    context = {
        'sectors': sectors,
        'posts': posts
    }
    return render(request, 'main.html', {'context': context})


@require_http_methods(["GET"])
def subsector_post(request):
    subsector_id = request.GET.get('subsector_id', None)
    if not subsector_id:
        return render(request, '404page.html')
    posts = (Post.objects
             .filter(subsector=subsector_id)
             .order_by('-created_at')
             .prefetch_related('subsector', 'user')
             )
    first_post = posts.first()
    if not first_post:
        return render(request, '404page.html')
    subsector = {
        'id': subsector_id,
        'title': first_post.subsector.title,
        'description': first_post.subsector.description,
        'sector_title': first_post.subsector.sector,
        'posts': []
    }
    post_id = 0
    for post in posts:
        subsector['posts'].append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'likes': post.likes,
            'dislikes': post.dislikes,
            'language': post.language,
        })
        if post.anonymously:
            subsector['posts'][post_id]['user'] = 'Anonymous'
            subsector['posts'][post_id]['user_image'] = 'user_photos/anon.PNG'
            subsector['posts'][post_id]['mark'] = None
        else:
            subsector['posts'][post_id]['user'] = post.user.username
            subsector['posts'][post_id]['user_image'] = post.user.photo
            subsector['posts'][post_id]['mark'] = post.user.mark
        post_id +=1

    return render(request, 'subsector.html', {'subsector': subsector})

def post_create(request):
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
            return render(request, 'post_form.html', {'sectors':sectors})
        refresh_token = request.COOKIES.get('refreshToken', None)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = HttpResponseRedirect(reverse('profile'))
            response.set_cookie('accessToken', access_token, httponly=True,secure=True)
            return response
        except TokenError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return redirect('login_rend')