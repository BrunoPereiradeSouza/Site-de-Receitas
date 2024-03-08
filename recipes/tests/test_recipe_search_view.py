from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

    # Start of view search tests
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))

        self.assertIs(view.func, views.search)

    def test_recipe_search_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))

        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')

        self.assertIn(
            '<title> Search for &quot;teste&quot; |  Recipes</title>',
            response.content.decode('utf-8')
            )
