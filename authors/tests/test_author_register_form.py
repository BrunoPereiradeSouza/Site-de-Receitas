from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


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
        ('username', 'Obrigatório. 150 caracteres ou menos. '
         'Letras, números e @/./+/-/_ apenas.'
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
