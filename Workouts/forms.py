from django import forms
from .models import WorkoutSet

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = WorkoutSet
        fields = ['exercise','reps','weight']
