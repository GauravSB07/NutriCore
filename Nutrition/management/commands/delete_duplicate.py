import csv
from django.core.management.base import BaseCommand
from Nutrition.models import Food, Category
from django.db.models import Count


class Command(BaseCommand):
    help = "Sync DB with CSV (remove duplicates + remove extra foods)"

    def handle(self, *args, **kwargs):

        file_path = "foods.csv"

        csv_names = set()

        # ✅ STEP 1: READ CSV
        with open(file_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = row["name"].strip().title()
                csv_names.add(name)

        # ✅ STEP 2: DELETE FOODS NOT IN CSV
        Food.objects.exclude(name__in=csv_names).delete()
        self.stdout.write("🗑 Removed foods not in CSV")

        # ✅ STEP 3: REMOVE DUPLICATES
        duplicates = (
            Food.objects.values('name')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        for dup in duplicates:
            foods = Food.objects.filter(name=dup['name'])
            foods.exclude(id=foods.first().id).delete()

        self.stdout.write("🧹 Removed duplicates")

        # ✅ STEP 4: UPDATE/CREATE FROM CSV
        with open(file_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = row["name"].strip().title()

                food, created = Food.objects.update_or_create(
                    name=name,
                    defaults={
                        "calories_per_100g": row["calories_per_100g"] or None,
                        "protein_per_100g": row["protein_per_100g"] or None,
                        "calories_per_unit": row["calories_per_unit"] or None,
                        "protein_per_unit": row["protein_per_unit"] or None,
                        "unit_type": row["unit_type"] or "g",
                        "serving_name": row["serving_name"] or None,
                        "serving_quantity": row["serving_quantity"] or None,
                    }
                )

                # categories
                food.categories.clear()
                categories = row["categories"].split(";") if row["categories"] else []

                for cat_name in categories:
                    cat_name = cat_name.strip()
                    if not cat_name:
                        continue

                    category, _ = Category.objects.get_or_create(name=cat_name)
                    food.categories.add(category)

        self.stdout.write(self.style.SUCCESS("✅ DB synced exactly with CSV"))