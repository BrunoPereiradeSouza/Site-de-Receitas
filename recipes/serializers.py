from rest_framework import serializers
from tag.models import Tag
from collections import defaultdict
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
            'tag_objects', 'tag_links'
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
        title = attrs['title']
        description = attrs['description']
        my_errors = defaultdict(list)

        if title == description:
            my_errors['title'].append('cannot be equal to description')
            my_errors['description'].append('cannot be equal to title')
        if my_errors:
            raise serializers.ValidationError(my_errors)

        return super().validate(attrs)

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('title must be greater than 5')
        return value

    def validate_description(self, value):
        print(value)
        return value
