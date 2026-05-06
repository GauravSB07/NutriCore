from django.urls import path
from .views import (
    log_meal,
    meal_list,
    delete_meal,
    edit_meal,
    food_detail,
    food_list,
    add_cheat_meal,
    log_water
)

app_name = 'nutrition'

urlpatterns = [
    path('log/', log_meal, name='log_meal'),
    path('list/', meal_list, name='meal_list'),
    path('delete/<int:id>/', delete_meal, name='delete_meal'),
    path('edit/<int:id>/', edit_meal, name='edit_meal'),

    path('foods/', food_list, name='food_list'),
    path('foods/<int:id>/', food_detail, name='food_detail'),

    path('cheat/<int:food_id>/', add_cheat_meal, name='add_cheat_meal'),

    path('water/', log_water, name='log_water'),
]