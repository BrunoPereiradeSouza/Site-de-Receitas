from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
            ('username', 'Your username'),
            ('email', 'Your e-mail'),
            ('first_name', 'Ex.: John'),
            ('last_name', 'Ex.: Doe'),
            ('password', 'Your password'),
            ('password2', 'Repeat your password'),
        ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        placeholder_field = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, placeholder_field)

    @parameterized.expand([
        ('username', 'Username must have letters, numbers or one of'
                     ' those @.+-_. The lenght should between 4 and 150'
                     'characters.'
         ),
        ('email', 'the e-mail must be valid.'),
        ('password', 'Password must have at least one uppercase letter'
         ', one lowercase letter and one number. The length should be at'
         ' least 8 characters'),
    ])
    def test_fields_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current_placeholder = form[field].field.help_text

        self.assertEqual(help_text, current_placeholder)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label

        self.assertEqual(label, current_label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            'first_name': 'first',
            'last_name': 'last',
            'username': 'user',
            'email': 'user@email.com',
            'password': 'Abc123456',
            'password2': 'Abc123456',
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'Password must not be empty'),
        ('first_name', 'First name must not be empty'),
        ('last_name', 'Last name must not be empty'),
        ('email', 'E-mail must not be empty'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'eu'
        error_msg = ('Username must have at least 4 characters')

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(error_msg, response.content.decode('utf-8'))
        self.assertIn(error_msg, response.context['form'].errors.get('username'))  # Noqa: E501

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'eu' * 76
        error_msg = ('Username cannot have more than 150 characters')

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(error_msg, response.content.decode('utf-8'))
        self.assertIn(error_msg, response.context['form'].errors.get('username'))  # Noqa: E501

    def test_password_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        error_mgs = ('Password must have at least one uppercase letter, '
                     'one lowercase letter and one number. The length should'
                     ' be at least 8 characters')

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(error_mgs, response.context['form'].errors.get('password'))  # Noqa: E501

    def test_password_and_password2_must_be_equal(self):
        self.form_data['password'] = 'Acd321212'
        error_msg = 'password and password2 must be equal'

        url = reverse('authors:create')
        response1 = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(error_msg, response1.context['form'].errors.get('password'))  # Noqa: E501

        self.form_data['password2'] = 'Acd321212'
        response2 = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(error_msg, response2.context['form'].errors)
        self.assertNotIn(error_msg, response2.content.decode('utf-8'))
