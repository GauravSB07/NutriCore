from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localdate

class StepsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.IntegerField()
    date = models.DateField(default=localdate)

    def __str__(self):
        return f"{self.user} - {self.steps} steps"