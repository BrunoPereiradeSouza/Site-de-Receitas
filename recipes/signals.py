import os
from django.dispatch import receiver
from recipes.models import Recipe
from django.db.models.signals import pre_save, pre_delete


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.get(pk=instance.pk)
    delete_cover(old_instance)