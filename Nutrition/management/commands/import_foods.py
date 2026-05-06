import csv
from django.core.management.base import BaseCommand
from Nutrition.models import Food, Category


class Command(BaseCommand):
    help = "Import or update foods from CSV (no duplicates)"

    def handle(self, *args, **kwargs):

        file_path = "foods.csv"

        with open(file_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:

                name = row["name"].strip()

                # 🔥 UPDATE OR CREATE (NO DUPLICATES)
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

                # ✅ HANDLE IMAGE
                image_path = row.get("image")

                if image_path:
                    image_path = image_path.strip().replace("\\", "/")

                    if "media/" in image_path:
                        image_path = image_path.split("media/")[-1]

                    if not image_path.startswith("foods/"):
                        image_path = f"foods/{image_path.split('/')[-1]}"

                    food.image = image_path
                    food.save()

                # ✅ HANDLE CATEGORIES (RESET + ADD)
                food.categories.clear()

                categories = row["categories"].split(";") if row["categories"] else []

                for cat_name in categories:
                    cat_name = cat_name.strip()

                    if not cat_name:
                        continue

                    category, _ = Category.objects.get_or_create(name=cat_name)
                    food.categories.add(category)

                # 🔥 LOG OUTPUT
                if created:
                    self.stdout.write(f"✔ Created: {food.name}")
                else:
                    self.stdout.write(f"🔄 Updated: {food.name}")

        self.stdout.write(self.style.SUCCESS("✅ Import completed (no duplicates)"))