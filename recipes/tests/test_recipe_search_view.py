from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

    # Start of view search tests
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))

        self.assertIs(view.func.view_class, views.RecipeListViewSearch)

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

    def test_recipe_search_loads_recipes_by_recipe_title(self):
        recipe1 = self.make_recipe(
            title='This is recipe one', author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(title='This is recipe two', slug='this-is')

        search_irl = reverse('recipes:search')

        response1 = self.client.get(f'{search_irl}?q={recipe1.title}')
        response2 = self.client.get(f'{search_irl}?q={recipe2.title}')
        response3 = self.client.get(f'{search_irl}?q=recipe')

        self.assertIn(recipe1.title, response1.content.decode('utf-8'))
        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2.title, response2.content.decode('utf-8'))
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response3.context['recipes'])
        self.assertIn(recipe2, response3.context['recipes'])
