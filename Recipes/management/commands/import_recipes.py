import csv
from django.core.management.base import BaseCommand
from Recipes.models import Recipe, RecipeCategory


class Command(BaseCommand):
    help = 'Import or update recipes from CSV'

    def handle(self, *args, **kwargs):
        with open('recipes.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                category_name = row.get('category', '').strip()

                category, _ = RecipeCategory.objects.get_or_create(
                    name=category_name
                )

                # 🔥 SAFE VALUES
                name = row.get('name', '').strip()

                calories = float(row.get('calories') or 0)
                protein = float(row.get('protein') or 0)

                ingredients = row.get('ingredients', '').strip()
                method = row.get('method', '').strip()
                tips = row.get('tips', '').strip()

                # 🔥 UPDATE OR CREATE (NO DUPLICATES)
                recipe, created = Recipe.objects.update_or_create(
                    name=name,   # 🔑 unique identifier
                    defaults={
                        'category': category,
                        'calories': calories,
                        'protein': protein,
                        'ingredients': ingredients,
                        'method': method,
                        'tips': tips
                    }
                )

                if created:
                    self.stdout.write(f"➕ Created: {name}")
                else:
                    self.stdout.write(f"🔄 Updated: {name}")

        self.stdout.write(self.style.SUCCESS("✅ Recipes Synced Successfully"))