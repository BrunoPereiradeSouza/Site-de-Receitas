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
    def test_first_name_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        placeholder_field = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, placeholder_field)
