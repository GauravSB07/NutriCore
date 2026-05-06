from django.contrib import admin
from .models import Recipe, RecipeCategory


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'calories', 'protein']
    search_fields = ['name']
    list_filter = ['category']


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']