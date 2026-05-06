from django.db import models

class RecipeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)

    category = models.ForeignKey(RecipeCategory, on_delete=models.SET_NULL, null=True)

    calories = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)

    price = models.FloatField(blank=True, null=True)

    ingredients = models.TextField(blank=True,default="")   # ✅ MERGED HERE
    method = models.TextField()
    tips = models.TextField(blank=True,null=True)



    def __str__(self):
        return self.name
