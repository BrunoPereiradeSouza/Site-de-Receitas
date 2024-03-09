from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Recipe
from django.db.models import Q
from django.http import Http404
from utils.pagination import make_pagination
import os

PER_PAGE = os.environ.get('PER_PAGE', 6)


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination = make_pagination(recipes, PER_PAGE, request)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination': pagination
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True).order_by('-id')
            )

    page_obj, pagination = make_pagination(recipes, PER_PAGE, request)

    return render(
        request, 'recipes/pages/category.html',
        context={
            'recipes': page_obj,
            'pagination': pagination}
        )


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()
    querry = ' '.join(search_term.split())
    page_title = f'Search for "{querry}"'
    if not querry:
        raise Http404

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=querry) |
            Q(description__icontains=querry)
        ),
        is_published=True
        ).order_by('-id')

    page_obj, pagination = make_pagination(recipes, PER_PAGE, request)

    context = {
        'querry': querry, 'page_title': page_title,
        'recipes': page_obj, 'pagination': pagination,
        'additional_url_querry': f'&q={search_term}'
          }
    return render(request, 'recipes/pages/search.html', context)
