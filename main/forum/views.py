from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.utils.mediatypes import order_by_precedence

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
                # 'description':subsector.description
            })
        sec_id += 1
    posts_data = (Post.objects
                  .all()
                  .order_by('-created_at')
                  .prefetch_related('subsector', 'user'))
    posts = []
    for post in posts_data:
        posts.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'likes': post.likes,
            'dislikes': post.dislikes,
            'language': post.language,
            'user': post.user.username,
            'user_image': post.user.photo,

            'subsector_title': post.subsector.title,
            'subsector_id': post.subsector.id,
            'sector_id': post.subsector.sector,
        })
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
    for post in posts:
        subsector['posts'].append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'likes': post.likes,
            'dislikes': post.dislikes,
            'language': post.language,
            'user': post.user.username,
            'user_image': post.user.photo,
        })

    return render(request, 'subsector.html', {'subsector': subsector})
