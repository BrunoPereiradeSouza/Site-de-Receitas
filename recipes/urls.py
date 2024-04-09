from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),  # noqa: E501
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name='category'),  # noqa: E501
    path('recipes/<int:id>/', views.recipe, name='recipe'),
]
