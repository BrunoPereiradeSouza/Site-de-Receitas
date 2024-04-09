from django.views.generic import ListView
from recipes.models import Recipe
from utils.pagination import make_pagination
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    template_name = 'recipes/pages/home.html'
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination = make_pagination(
            context.get('recipes'), PER_PAGE, self.request
        )
        context.update({'recipes': page_obj, 'pagination': pagination})

        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'
