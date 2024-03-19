from django import forms
from django.contrib.auth.models import User
from utils import django_forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        django_forms.add_placeholer(self.fields['username'], 'Your username')
        django_forms.add_placeholer(self.fields['email'], 'Your e-mail')
        django_forms.add_placeholer(self.fields['first_name'], 'Ex.: John')
        django_forms.add_placeholer(self.fields['last_name'], 'Ex.: Doe')
        django_forms.add_placeholer(self.fields['password'], 'Your password')
        django_forms.add_placeholer(self.fields['password2'], 'Repeat your password')  # Noqa: E501

    username = forms.CharField(
        error_messages={
            'required': 'Username must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username cannot have more than 150 characters'
        },
        label='Username',
        help_text=('Username must have letters, numbers or one of'
                   ' those @.+-_. The lenght should between 4 and 150'
                   'characters.'
                   ),
        min_length=4, max_length=150
    )

    first_name = forms.CharField(
        widget=forms.TextInput(),
        error_messages={
            'required': 'First name must not be empty'
        },
        label='First name'
    )

    last_name = forms.CharField(
        widget=forms.TextInput(),
        error_messages={
            'required': 'Last name must not be empty'
        },
        label='Last name'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(),
        error_messages={
            'required': 'E-mail must not be empty'
        },
        help_text=('the e-mail must be valid.'),
        label='E-mail',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, one lowercase'
            ' letter and one number. The length should be at least 8 characters'  # Noqa: E501
        ),
        validators=[django_forms.strong_password],
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password2',
        error_messages={
            'required': 'Please, repeat your password'
        },
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'email already exists',
            )

        return email

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
