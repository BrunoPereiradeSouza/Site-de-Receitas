from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewsTest(TestCase):
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
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com'
        )
        recipe = Recipe.objects.create(
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time='20',
            preparation_time_unit='Minutos',
            servings='10',
            servings_unit='Pessoas',
            preparation_steps='Lorem ipsun dolor sit amet',
            preparation_steps_is_html=False,
            is_published=True,
            category=category,
            author=author,
        )

        response = self.client.get(reverse('recipes:home'))
        self.assertIn(recipe.title, response.content.decode('utf-8'))
        self.assertTrue(response.context['recipes'])

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_function_return_404_if_no_recipes_found(self):  # noqa: E501
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_recipes_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_recipes_view_function_return_404_if_no_recipe_found(self):  # noqa: E501
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)
