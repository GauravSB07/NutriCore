# control_panel/forms.py
from django.forms import ModelForm
from Workouts.models import Exercise,MuscleGroup,SubMuscle
from Nutrition.models import Category,MealLog,Food
from Recipes.models import Recipe,RecipeCategory
from Users.models import Profile

class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class MealLogForm(ModelForm):
    class Meta:
        model = MealLog
        fields = '__all__'

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeCategoryForm(ModelForm):
    class Meta:
        model = RecipeCategory
        fields = '__all__'

class MuscleGroupForm(ModelForm):
    class Meta:
        model = MuscleGroup
        fields = '__all__'


class SubMuscleForm(ModelForm):
    class Meta:
        model = SubMuscle
        fields = '__all__'

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 ADD IDS HERE (NO TEMPLATE FILTER NEEDED)
        self.fields['user'].widget.attrs.update({'id': 'userSelect'})
        self.fields['height'].widget.attrs.update({'id': 'height'})
        self.fields['weight'].widget.attrs.update({'id': 'weight'})
        self.fields['start_weight'].widget.attrs.update({'id': 'start_weight'})
        self.fields['target_weight'].widget.attrs.update({'id': 'target_weight'})
        self.fields['daily_steps_target'].widget.attrs.update({'id': 'steps'})
        self.fields['daily_calorie_target'].widget.attrs.update({'id': 'calories'})
        self.fields['daily_protein_target'].widget.attrs.update({'id': 'protein'})
        self.fields['max_cheat_calories_per_day'].widget.attrs.update({'id': 'cheat_cal'})
        self.fields['max_cheat_meals_per_day'].widget.attrs.update({'id': 'cheat_meals'})
        self.fields['goal'].widget.attrs.update({'id': 'goal'})
        self.fields['points'].widget.attrs.update({'id': 'points'})
        self.fields['daily_water_goal'].widget.attrs.update({'id': 'water'})
        self.fields['is_onboarded'].widget.attrs.update({'id': 'onboarded'})