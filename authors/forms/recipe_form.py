from django.core.exceptions import ValidationError
from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict
from authors.validators import AuthorRecipeValidator


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
                 'preparation_time_unit', 'servings', 'servings_unit', \
                 'preparation_steps', 'cover',
        widgets = {
            'cover': forms.FileInput(attrs={'class': 'span-2'}),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('porções', 'porções'),
                    ('pedaços', 'pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
        }

    def clean(self):
        super_clean = super().clean()
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
