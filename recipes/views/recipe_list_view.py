from django.views.generic import ListView
from recipes.models import Recipe
from django.http import Http404
from django.http import JsonResponse
from utils.pagination import make_pagination
from django.db.models import Q
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


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category_id=self.kwargs.get('category_id'),
        )

        if not qs:
            raise Http404

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_title = f'{context.get("recipes")[0].category.name} ' \
            '- Category | '

        context.update(
            {
                'page_title': page_title,
            }
        )

        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()
        querry = ' '.join(search_term.split())
        qs = qs.filter(
            Q(
                Q(title__icontains=querry) |
                Q(description__icontains=querry)
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()
        querry = ' '.join(search_term.split())
        page_title = f'Search for "{querry}"'

        if not search_term:
            raise Http404

        context.update(
            {
                'page_title': page_title,
                'additional_url_querry': f'&q={search_term}',
                'querry': querry
            }
        )
        return context