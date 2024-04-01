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

    def get_form(self):
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        return form

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

        email_field = form.find_element(
            By.XPATH,
            '//input[@placeholder="Your e-mail"]'
        )
        email_field.send_keys('email@invalid')

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.fill_form_dummy_data(form)

        callback(form)
        return form

    def form_field_test_error_messages(self, placeholder, error_message):
        def callback(form):
            field = self.get_by_placeholder(form, placeholder)
            field.send_keys(' ' * 10)
            field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn(error_message, form.text)
            sleep(5)
        self.form_field_test_with_callback(callback)

    def test_empty_first_name_error_message(self):
        self.form_field_test_error_messages(
            'Ex.: John',
            'First name must not be empty'
            )

    def test_empty_last_name_error_message(self):
        self.form_field_test_error_messages(
            'Ex.: Doe',
            'Last name must not be empty'
        )

    def test_empty_username_error_message(self):
        self.form_field_test_error_messages(
            'Your username',
            'Username must not be empty'
        )

    def test_invalid_email(self):
        self.form_field_test_error_messages(
            'Your e-mail',
            'Informe um endereço de email válido.'
        )

    def test_empty_password_error_message(self):
        self.form_field_test_error_messages(
            'Your password',
            'Password must not be empty'
        )

    def test_empty_password2_error_message(self):
        self.form_field_test_error_messages(
            'Repeat your password',
            'Please, repeat your password'
        )
