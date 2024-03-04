from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com'
        )
        recipe = Recipe.objects.create(
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time='20',
            preparation_time_unit='Minutos',
            servings='10',
            servings_unit='Pessoas',
            preparation_steps='Lorem ipsun dolor sit amet',
            preparation_steps_is_html=False,
            is_published=True,
            category=category,
            author=author,
        )
        return super().setUp()
