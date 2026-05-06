from django.contrib import admin
from .models import Food,MealLog,Category

# Register your models here.

class FoodAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories',)
    search_fields = ['name']

admin.site.register(Food , FoodAdmin)
admin.site.register(MealLog)
admin.site.register(Category)