from django.views import View
from recipes.models import Recipe
from authors.forms import AuthorRecipeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse


class DashboardRecipe(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(
            author=request.user, is_published=False, id=id
        )

        if request.method == 'POST':
            form = AuthorRecipeForm(
                request.POST or None,
                request.FILES or None,
                instance=recipe
            )
            if form.is_valid():
                recipe = form.save(commit=False)

                recipe.author = request.user
                recipe.preparation_steps_is_html = False
                recipe.is_published = False
                recipe.save()

                messages.success(request, 'Sua receita foi salva com sucesso!')
                return redirect(reverse(
                    'authors:dashboard_recipe_edit', args=(id,)
                    )
                )
        else:
            form = AuthorRecipeForm(instance=recipe)

        return render(request, 'authors/pages/dashboard_recipe.html', context={
            'form': form
        })
