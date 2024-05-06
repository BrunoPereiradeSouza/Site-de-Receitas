from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe.objects.create(
            title='Recipe Title New',
            description='Recipe Description',
            slug='recipe-title-new',
            preparation_time='20',
            preparation_time_unit='Minutos',
            servings='10',
            servings_unit='Pessoas',
            preparation_steps='Lorem ipsun dolor sit amet',
            category=self.make_category(name='New category default'),
            author=self.make_author(username='newuser'),
        )

        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_lenght(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False',
            )

    def test_recipe_is_publisehd_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False',
            )

    def test_recipe_string_representation_is_title_field(self):
        needed = 'Testing representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()

        self.assertEqual(str(self.recipe), needed)
