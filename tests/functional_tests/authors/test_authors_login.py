from .base import AuthorsBaseFunctionalTest
import pytest
from selenium.webdriver.common.by import By
from django.urls import reverse


@pytest.mark.functional_test
class AuthorLoginFunctionalTest(AuthorsBaseFunctionalTest):

    def test_login_user_is_sucessfully(self):
        self.register_valid_user()

        # Usuário abre a página
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        # Usuário ver o input de username e digita 'MyUsername'
        username.send_keys('MyUsername')

        # Usuário ver o input de password e digita 'Abc123456'
        password.send_keys('Abc123456')

        # Usuário confirma o login
        form.submit()

        # Usuário vê a mensagem de login com sucesso e seu username
        self.assertIn(
            'Your are logged in with MyUsername',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )
        self.sleep()
