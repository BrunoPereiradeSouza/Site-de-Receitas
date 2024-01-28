from django.contrib import admin
from .models import Category, Recipe


admin.site.register(Category)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...