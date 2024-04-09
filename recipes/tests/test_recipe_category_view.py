from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

    # Start of view category tests
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))

        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_loads_correct_template(self):
        recipe = self.make_recipe()
        response = self.client.get(reverse(
            'recipes:category', kwargs={'category_id': recipe.category.id}
            ))

        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_recipe_category_template_loads_recipes(self):
        recipe = self.make_recipe()
        response = self.client.get(reverse(
            'recipes:category', kwargs={'category_id': recipe.category.id}
            ))

        self.assertIn(recipe.title, response.content.decode('utf-8'))

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category',
                    kwargs={'category_id': recipe.category.id})
            )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_function_return_404_if_no_recipes_found(self):  # noqa: E501
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))

        self.assertEqual(response.status_code, 404)
    # End of view category tests
