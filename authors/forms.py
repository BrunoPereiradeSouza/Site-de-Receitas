from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholer(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, one lowercase'
            ' letter and one number. The length should be at least 8 characters'  # Noqa:E501
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholer(self.fields['username'], 'Your username')
        add_placeholer(self.fields['email'], 'Your e-mail')
        add_placeholer(self.fields['first_name'], 'Ex.: John')
        add_placeholer(self.fields['last_name'], 'Ex.: Doe')
        add_placeholer(self.fields['password'], 'Your password')
        add_placeholer(self.fields['password2'], 'Repeat your password')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password mut not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, one lowercase'
            ' letter and one number. The length should be at least 8 characters'  # Noqa: E501
        ),
        validators=[strong_password],
        label='Password'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Password2'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
              ]

        # serve para definir o nome que será exibido no label de cada campo
        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            
        }

        # Definir mensagens de ajuda nos campos
        help_texts = {
            'email': 'the e-mail must be valid.',
        }

        # Definir mensagens de erro nos campos
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'password and password2 must be equal',
                code='invalid'
            )
            
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ]
            }
            )
