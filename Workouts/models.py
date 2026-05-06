from django.db import models
from django.contrib.auth.models import User

class MuscleGroup(models.Model):
    name = models.CharField(max_length=100)

    image = models.ImageField(upload_to='muscles/', blank=True, null=True)

    def __str__(self):
        return self.name


class SubMuscle(models.Model):
    name = models.CharField(max_length=100)
    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.CASCADE,
        related_name='sub_muscles'
    )

    # 🔥 ADD THESE
    description = models.TextField(blank=True)
    video = models.FileField(upload_to='submuscles/', blank=True, null=True)

    image = models.ImageField(upload_to='submuscles/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.muscle_group} - {self.name}"


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    video = models.FileField(upload_to='exercises/', blank=True, null=True)
    image = models.ImageField(upload_to='exercise_images/', blank=True, null=True)
    description = models.TextField(blank=True)

    steps = models.TextField(blank=True, help_text="Write each step on a new line")
    equipment = models.CharField(max_length=200, blank=True)



    sub_muscle = models.ForeignKey(
        SubMuscle,
        on_delete=models.CASCADE,
        related_name='exercises'
    )

    def __str__(self):
        return self.name

class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 🔥 REPLACE THIS
    sub_muscle = models.ForeignKey(
        SubMuscle,
        on_delete=models.CASCADE,
        related_name='sessions'
    )

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.sub_muscle}"
    
    
class WorkoutSet(models.Model):
    session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
        related_name='sets'
    )

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    sub_muscle = models.ForeignKey(   
        SubMuscle,
        on_delete=models.CASCADE
    )

    set_number = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.exercise} Set {self.set_number}"