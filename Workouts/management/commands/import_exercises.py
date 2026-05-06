import csv
from django.core.management.base import BaseCommand
from Workouts.models import Exercise, MuscleGroup, SubMuscle


class Command(BaseCommand):
    help = "Import exercises (clean CSV only)"

    def handle(self, *args, **kwargs):

        file_path = "exercises.csv"

        with open(file_path, newline='', encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:

                name = row["name"].strip()
                muscle_data = row["muscle"].strip()

                if "-" not in muscle_data:
                    self.stdout.write(f"❌ Skipped bad format: {name}")
                    continue

                muscle_name, sub_name = [x.strip() for x in muscle_data.split("-", 1)]

                muscle, _ = MuscleGroup.objects.get_or_create(name=muscle_name)

                sub_muscle, _ = SubMuscle.objects.get_or_create(
                    name=sub_name,
                    muscle_group=muscle
                )

                exercise, created = Exercise.objects.update_or_create(
                    name=name,
                    defaults={"sub_muscle": sub_muscle}
                )

                if created:
                    self.stdout.write(f"✔ Created: {name}")
                else:
                    self.stdout.write(f"🔄 Updated: {name}")

        self.stdout.write(self.style.SUCCESS("✅ Clean import done"))