from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import RecipeBaseFunctionalTest
import pytest
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 😢', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(10)

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre a página home
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto "search for a recipe..."
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe..."]'
            )

        # Clica nesse input e digita o termo de busca "Reipe title 1"
        # para encontrar a receita com esse título
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)
        self.sleep(5)

        # Usuário vê o que estava procurando na página
        body = self.browser.find_element(By.CLASS_NAME, 'main-content-list')
        self.assertIn(title_needed, body.text)

    @patch('recipes.views.recipe_list_view.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # Usuário abre a página home
        self.browser.get(self.live_server_url)

        # Usuário vê uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Vê que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
