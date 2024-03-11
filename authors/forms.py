from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholer(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholer(self.fields['username'], 'Your username')
        add_placeholer(self.fields['email'], 'Your e-mail')
        add_placeholer(self.fields['first_name'], 'Ex.: John')
        add_placeholer(self.fields['last_name'], 'Ex.: Doe')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password mut not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, one lowercase'
            ' letter and one number. The length should be at least 8 characters'  # Noqa: E501
        )
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
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
            'password': 'Password',
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

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username here',
                'class': 'form-control',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(value)s no campo password',
                code='invalid',
                params={'value': '"atenção"'}
                )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={'value': '"John Doe"'}
                )

        return data
