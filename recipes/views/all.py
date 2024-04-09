from django.shortcuts import render, get_object_or_404
from recipes.models import Recipe
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })
