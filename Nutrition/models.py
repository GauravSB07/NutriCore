from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localdate

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Food(models.Model):
    name = models.CharField(max_length=100)

    calories_per_100g = models.FloatField(null=True, blank=True)
    protein_per_100g = models.FloatField(null=True, blank=True)

    calories_per_unit = models.FloatField(null=True, blank=True)
    protein_per_unit = models.FloatField(null=True, blank=True)

    UNIT_CHOICES = [
        ('g', 'Grams'),
        ('ml', 'Milliliters'),
        ('unit', 'Per Piece'),
    ]

    unit_type = models.CharField(max_length=10, choices=UNIT_CHOICES, default='g')

    # 🔥 ADD THIS (serving system)
    serving_name = models.CharField(max_length=50, null=True, blank=True)
    serving_quantity = models.FloatField(null=True, blank=True)

    image = models.ImageField(upload_to='foods/', null=True, blank=True)

    categories = models.ManyToManyField(Category, related_name='foods', blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class MealLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    quantity = models.FloatField()
    unit = models.CharField(max_length=10, default='g')   # ✅ ADD THIS

    date = models.DateField(default=localdate)
    is_cheat = models.BooleanField(default=False)

    calories = models.FloatField(blank=True)
    protein = models.FloatField(blank=True)

    def save(self, *args, **kwargs):

        qty = self.quantity or 0
        unit = self.unit
        food = self.food

        # ✅ SAFE VALUES (FIXES YOUR ERROR)
        cal100 = food.calories_per_100g or 0
        prot100 = food.protein_per_100g or 0
        calUnit = food.calories_per_unit or 0
        protUnit = food.protein_per_unit or 0

        # 🔥 SERVING CONVERSION
        if unit == 'serving' and food.serving_quantity:
            qty = qty * food.serving_quantity
            unit = food.unit_type

        # 🔹 CALCULATION
        if unit in ['g', 'ml']:
            self.calories = (cal100 / 100) * qty
            self.protein = (prot100 / 100) * qty
        else:
            self.calories = calUnit * qty
            self.protein = protUnit * qty

        super().save(*args, **kwargs)

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()  # in ml
    date = models.DateField(default=localdate)

    def __str__(self):
        return f"{self.user} - {self.amount}ml"


