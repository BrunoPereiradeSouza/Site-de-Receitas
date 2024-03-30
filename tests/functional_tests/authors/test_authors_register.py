from .base import AuthorsBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class AuthorsRegisterFunctionalTest(AuthorsBaseFunctionalTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

        email_field = form.find_element(
            By.XPATH,
            '//input[@placeholder="Your e-mail"]'
        )
        email_field.send_keys('email@email.com')

    def test_empty_first_name_error_message(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        self.fill_form_dummy_data(form)
        first_name_field = self.get_by_placeholder(
            web_element=form,
            placeholder="Ex.: John"
            )
        first_name_field.send_keys(' ')
        first_name_field.send_keys(Keys.ENTER)
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        self.assertIn('First name must not be empty', form.text)
        sleep(5)
