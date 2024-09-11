from django.shortcuts import render
from rest_framework.generics import get_object_or_404
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
        print(sectors)
    return render(request, 'main.html', {'sectors': sectors})


@require_http_methods(["GET"])
def subsector_post(request):
    subsector_id = request.GET.get('subsector_id', None)
    sector_id = request.GET.get('sector_id', None)
    sector_title = request.GET.get('sector_title', None)
    if (not subsector_id) or (not sector_id) or (not sector_title):
        return render(request, '404page.html')
    posts = (Post.objects
             .filter(subsector=subsector_id)
             .order_by('-created_at')
             .prefetch_related('subsector')
             )
    first_post = posts.first()
    if not first_post:
        return render(request, '404page.html')
    subsector = {
        'id': subsector_id,
        'title': first_post.subsector.title,
        'description': first_post.subsector.description,
        'sector': {
            'id': sector_id,
            'title': sector_title
        },
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
        })

    return render(request, 'subsector.html', {'subsector': subsector})
