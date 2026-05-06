from django.core.management.base import BaseCommand
from Nutrition.models import Category

class Command(BaseCommand):
    help = "Create default categories"

    def handle(self, *args, **kwargs):
        cats = [
            "Veg","Non-Veg","Egg",
            "High Protein","High Carb","Low Calorie","Healthy","Junk",
            "Indian","Street Food","Fast Food","Snacks","Desserts",
            "Beverages","South Indian","Chinese"
        ]

        for c in cats:
            Category.objects.get_or_create(name=c)

        self.stdout.write(self.style.SUCCESS("✅ Categories created"))