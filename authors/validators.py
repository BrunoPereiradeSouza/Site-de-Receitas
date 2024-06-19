from django.core.exceptions import ValidationError
from collections import defaultdict
from utils.strings import is_positive


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self):
        self.clean_preparation_time()
        self.clean_servings()
        cleaned_data = self.data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        preparation_steps = cleaned_data.get('preparation_steps')

        if len(title) < 4:
            self.errors['title'].append(
                'Title must have at least 4 characteres.'
            )

        if len(description) < 10:
            self.errors['description'].append(
                'Description must have at least 10 characteres.'
            )
        try:
            if len(preparation_steps) < 50:
                self.errors['preparation_steps'].append(
                    'Preparation steps must have at least 50 characteres.'
                )
        except TypeError:
            ...

        if title == description:
            self.errors['title'].append(
                'Title cannot be equal to description'
                )
            self.errors['description'].append(
                'Description cannot be equal to title'
                )

        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.data.get(field_name)

        if not is_positive(field_value):
            self.errors[field_name].append(
                'preparation time must be greater than 0'
            )

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)

        if not is_positive(field_value):
            self.errors[field_name].append(
                'Servings must be greater than 0'
            )

        return field_value
