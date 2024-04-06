from django.core.exceptions import ValidationError
from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict
from utils.strings import is_positive


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
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        preparation_steps = cleaned_data.get('preparation_steps')

        if len(title) < 4:
            self._my_errors['title'].append(
                'Title must have at least 4 characteres.'
            )

        if len(description) < 10:
            self._my_errors['description'].append(
                'Description must have at least 10 characteres.'
            )

        if len(preparation_steps) < 50:
            self._my_errors['preparation_steps'].append(
                'Preparation steps must have at least 50 characteres.'
            )

        if title == description:
            self._my_errors['title'].append(
                'Title cannot be equal to description'
                )
            self._my_errors['description'].append(
                'Description cannot be equal to title'
                )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive(field_value):
            self._my_errors[field_name].append(
                'preparation time must be greater than 0'
            )

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive(field_value):
            self._my_errors[field_name].append(
                'Servings must be greater than 0'
            )

        return field_value
