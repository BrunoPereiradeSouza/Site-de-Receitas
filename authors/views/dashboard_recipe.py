from django.views import View
from recipes.models import Recipe
from authors.forms import AuthorRecipeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(
        login_required(login_url='authors:login', redirect_field_name='next'),
        name='dispatch'
    )
class DashboardRecipe(View):
    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.get(
                author=self.request.user, is_published=False, id=id
            )

            if not recipe:
                raise Http404

        return recipe

    def render_recipe(self, form):
        return render(
            self.request, 'authors/pages/dashboard_recipe.html',
            context={'form': form}
        )

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

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
                'authors:dashboard_recipe_edit', args=(recipe.id,)
                )
            )

        return self.render_recipe(form)
