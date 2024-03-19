from django import forms
from utils.django_forms import add_placeholer


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholer(self.fields['username'], 'Type your username')
        add_placeholer(self.fields['password'], 'Type your password')
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
