import csv
from django.core.management.base import BaseCommand
from Workouts.models import Exercise

class Command(BaseCommand):
    help = "Import exercise data from CSV"

    def handle(self, *args, **kwargs):
        with open('exercise_detail.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            updated = 0
            not_found = []

            for row in reader:
                name = row['name'].strip()

                try:
                    ex = Exercise.objects.get(name__iexact=name)

                    ex.description = row.get('description', '')
                    ex.steps = row.get('steps', '')
                    ex.equipment = row.get('equipment', '')

                    ex.save()
                    updated += 1

                except Exercise.DoesNotExist:
                    not_found.append(name)

            self.stdout.write(self.style.SUCCESS(f"✅ Updated: {updated} exercises"))

            if not_found:
                self.stdout.write(self.style.WARNING(f"⚠️ Not found: {not_found}"))