from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

    # Start of view home tests
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))

        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipe_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<h1>No recipes found here 😢</h1>',
            response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))

        self.assertIn('Recipe Title', response.content.decode('utf-8'))
        self.assertEqual(len(response.context['recipes']), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        context = response.context['recipes']

        self.assertEqual(len(context), 0)
        self.assertIn('<h1>No recipes found here 😢</h1>', content)
    # End of view home tests

    # Start of view category tests
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))

        self.assertIs(view.func, views.category)

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

    # Start of view recipe tests
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))

        self.assertIs(view.func, views.recipe)

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

    # Start of view search tests
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))

        self.assertIs(view.func, views.search)
