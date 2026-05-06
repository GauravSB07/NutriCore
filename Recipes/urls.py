from django.urls import path
from .views import recipe_list, recipe_detail

app_name = 'recipes'

urlpatterns = [
    path('', recipe_list, name='recipe_list'),
    path('<int:id>/', recipe_detail, name='recipe_detail'),
]