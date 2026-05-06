from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'goal',
            'weight',
            'height',
            'daily_calorie_target',
            'daily_protein_target',
            'daily_water_goal'
        ]