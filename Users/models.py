from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 🔥 ADD THIS
    height = models.FloatField(null=True, blank=True)  # in cm

    weight = models.FloatField(null=True, blank=True)
    start_weight = models.FloatField(null=True, blank=True)
    target_weight = models.FloatField(null=True, blank=True)

    daily_steps_target = models.IntegerField(default=0)

    daily_calorie_target = models.FloatField(default=2000)
    daily_protein_target = models.FloatField(default=80)

    max_cheat_calories_per_day = models.FloatField(default=300)
    max_cheat_meals_per_day = models.IntegerField(default=2)

    # 🔥 FIX GOAL (CLEAN)
    GOAL_CHOICES = [
        ('fat_loss', 'Fat Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('maintain', 'Maintain'),
    ]

    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='fat_loss')

    points = models.IntegerField(default=0)
    daily_water_goal = models.FloatField(default=3000)

    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    is_onboarded = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


