from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Recipe
from django.db.models import Q
from django.http import Http404


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True).order_by('-id')
            )
    return render(
        request, 'recipes/pages/category.html',
        context={'recipes': recipes}
        )


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_form = request.GET.get('q', '').strip()
    querry = ' '.join(search_form.split())
    page_title = f'Search for "{querry}"'
    if not querry:
        raise Http404

    recipes = Recipe.objects.filter(
        Q(title__icontains=querry) |
        Q(description__icontains=querry)
        ).order_by('-id')

    context = {'querry': querry, 'page_title': page_title, 'recipes': recipes}
    return render(request, 'recipes/pages/search.html', context)
