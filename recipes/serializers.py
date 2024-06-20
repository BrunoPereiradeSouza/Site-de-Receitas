from rest_framework import serializers
from tag.models import Tag
from authors.validators import AuthorRecipeValidator
from .models import Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'public',
            'preparation', 'category', 'author', 'tags',
            'tag_objects', 'tag_links', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit',
            'preparation_steps', 'cover'
        ]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField()
    tag_objects = TagSerializer(
        many=True, source='tags', read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('description') is None:
            attrs['description'] = self.instance.description
        if self.instance is not None and attrs.get('title') is None:
            attrs['title'] = self.instance.title
        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings
        super_validate = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError
            )
        return super_validate
