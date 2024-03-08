from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    # Start of view recipe tests
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))

        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_loads_correct_template(self):
        recipe = self.make_recipe()
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': recipe.id}
            ))

        self.assertTemplateUsed(response, 'recipes/pages/recipe-view.html')

    def test_recipe_detail_view_function_return_404_if_no_recipe_found(self):  # noqa: E501
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_load_the_correct_recipe(self):
        title = 'Titulo para teste'
        recipe = self.make_recipe(title=title)
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': recipe.id}
            ))

        self.assertIn(title, response.content.decode('utf-8'))

    def test_recipe_detail_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id})
            )

        self.assertEqual(response.status_code, 404)
    # End of view recipe tests
