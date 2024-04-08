from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeHomeViewTest(RecipeTestBase):

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

    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch(9)

        with patch('recipes.views.recipe_list_view.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)

    def test_invalid_page_uses_page_one(self):
        response = self.client.get(reverse('recipes:home') + '?page=2a')
        self.assertEqual(response.context['recipes'].number, 1)
