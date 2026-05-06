from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),

    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/add/', views.add_exercise, name='add_exercise'),

    path('exercises/edit/<int:id>/', views.edit_exercise, name='edit_exercise'),
    path('exercises/delete/<int:id>/', views.delete_exercise, name='delete_exercise'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:id>/', views.delete_category, name='delete_category'),

    path('meal-logs/', views.meal_log_list, name='meal_log_list'),
    path('meal-logs/add/', views.add_meal_log, name='add_meal_log'),
    path('meal-logs/edit/<int:id>/', views.edit_meal_log, name='edit_meal_log'),
    path('meal-logs/delete/<int:id>/', views.delete_meal_log, name='delete_meal_log'),

    path('foods/', views.food_list, name='food_list'),
    path('foods/add/', views.add_food, name='add_food'),
    path('foods/edit/<int:id>/', views.edit_food, name='edit_food'),
    path('foods/delete/<int:id>/', views.delete_food, name='delete_food'),

    # RECIPES
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/edit/<int:id>/', views.edit_recipe, name='edit_recipe'),
    path('recipes/delete/<int:id>/', views.delete_recipe, name='delete_recipe'),

    # RECIPE CATEGORIES
    path('recipe-categories/', views.recipe_category_list, name='recipe_category_list'),
    path('recipe-categories/add/', views.add_recipe_category, name='add_recipe_category'),
    path('recipe-categories/edit/<int:id>/', views.edit_recipe_category, name='edit_recipe_category'),
    path('recipe-categories/delete/<int:id>/', views.delete_recipe_category, name='delete_recipe_category'),

    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:id>/', views.delete_user, name='delete_user'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/add/', views.add_profile, name='add_profile'),
    path('profiles/edit/<int:id>/', views.edit_profile, name='edit_profile'),
    path('profiles/delete/<int:id>/', views.delete_profile, name='delete_profile'),
    
    # MUSCLE GROUPS
    path('muscle-groups/', views.muscle_group_list, name='muscle_group_list'),
    path('muscle-groups/add/', views.add_muscle_group, name='add_muscle_group'),
    path('muscle-groups/edit/<int:id>/', views.edit_muscle_group, name='edit_muscle_group'),
    path('muscle-groups/delete/<int:id>/', views.delete_muscle_group, name='delete_muscle_group'),

    # SUB MUSCLES
    path('sub-muscles/', views.sub_muscle_list, name='sub_muscle_list'),
    path('sub-muscles/add/', views.add_sub_muscle, name='add_sub_muscle'),
    path('sub-muscles/edit/<int:id>/', views.edit_sub_muscle, name='edit_sub_muscle'),
    path('sub-muscles/delete/<int:id>/', views.delete_sub_muscle, name='delete_sub_muscle'),
]