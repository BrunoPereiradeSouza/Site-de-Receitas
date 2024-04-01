from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By
from time import sleep


class AuthorsBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def sleep(self, qtd=5):
        sleep(qtd)

    def get_form(self):
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        return form

    def register_valid_user(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        first_name = self.get_by_placeholder(form, 'Ex.: John')
        first_name.send_keys('First Name')
        last_name = self.get_by_placeholder(form, 'Ex.: Doe')
        last_name.send_keys('Last Name')
        username = self.get_by_placeholder(form, 'Your username')
        username.send_keys('MyUsername')
        email = self.get_by_placeholder(form, 'Your e-mail')
        email.send_keys('Email@email.com')
        password = self.get_by_placeholder(form, 'Your password')
        password.send_keys('Abc123456')
        password2 = self.get_by_placeholder(form, 'Repeat your password')
        password2.send_keys('Abc123456')
        form.submit()
