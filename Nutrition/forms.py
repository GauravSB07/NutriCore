from django import forms
from .models import MealLog, Food

class MealLogForm(forms.ModelForm):
    food = forms.ModelChoiceField(
        queryset=Food.objects.all(),
        widget=forms.Select(attrs={'class': 'searchable'})
    )      
       
    is_cheat = forms.BooleanField(required=False,label="Mark as Cheat Meal")

    class Meta:
        model = MealLog
        fields = ['food', 'quantity', 'unit']
