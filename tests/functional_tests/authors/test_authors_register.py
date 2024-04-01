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

    def test_password_and_password2_must_be_equal_error_message(self):
        def callback(form):
            password = self.get_by_placeholder(form, 'Your password')
            password.send_keys(' PassWord1')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password2.send_keys(' PassWord2')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('password and password2 must be equal', form.text)
            sleep(5)
        self.form_field_test_with_callback(callback)

    def test_form_is_valid(self):
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

        self.assertIn(
            'Your user is created, please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )
