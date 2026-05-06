from django.shortcuts import render,redirect,get_object_or_404
from .decorators import admin_required
from Workouts.models import Exercise,MuscleGroup,SubMuscle
from .forms import ExerciseForm,CategoryForm,MealLogForm,FoodForm,RecipeForm,RecipeCategoryForm,ProfileForm
from Nutrition.models import Category,MealLog,Food
from Recipes.models import Recipe,RecipeCategory
from django.contrib.auth.models import User
from Users.models import Profile
from django.http import JsonResponse
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

@admin_required
def dashboard(request):
    return render(request, 'control_panel/dashboard.html')

@admin_required
def exercise_list(request):

    exercises = Exercise.objects.all().order_by('-id')

    query = request.GET.get('q')

    if query:
        exercises = exercises.filter(name__icontains=query)

    # 🔥 AJAX SEARCH
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        html = render_to_string(
            'control_panel/partials/exercise_items.html',
            {'exercises': exercises},
            request=request
        )

        return JsonResponse({
            'html': html,
            'count': exercises.count()
        })

    return render(request, 'control_panel/exercise_list.html', {
        'exercises': exercises
    })

@admin_required
def add_exercise(request):
    form = ExerciseForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('exercise_list')

    return render(request, 'control_panel/exercise_form.html', {'form': form})

@admin_required
def edit_exercise(request, id):
    exercise = get_object_or_404(Exercise, id=id)

    form = ExerciseForm(request.POST or None, request.FILES or None, instance=exercise)

    if form.is_valid():
        form.save()
        return redirect('exercise_list')

    return render(request, 'control_panel/exercise_form.html', {'form': form})

@admin_required
def delete_exercise(request, id):
    exercise = get_object_or_404(Exercise, id=id)
    exercise.delete()
    return redirect('exercise_list')


@admin_required
def category_list(request):
    categories = Category.objects.all().order_by('-id')

    return render(request, 'control_panel/category_list.html', {
        'categories': categories
    })


@admin_required
def add_category(request):
    form = CategoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'control_panel/category_form.html', {'form': form})


@admin_required
def edit_category(request, id):
    category = get_object_or_404(Category, id=id)

    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        form.save()
        return redirect('category_list')

    return render(request, 'control_panel/category_form.html', {'form': form})


@admin_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()

    return redirect('category_list')

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from datetime import datetime
from django.contrib.auth.decorators import login_required

@admin_required
def meal_log_list(request):
    meals = MealLog.objects.select_related('food', 'user').order_by('-date')

    date = request.GET.get('date')

    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            meals = meals.filter(date=date_obj)
        except:
            pass

    # 🔥 AJAX RESPONSE
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            'control_panel/partials/meal_items.html',
            {'meals': meals}
        )
        return JsonResponse({'html': html})

    return render(request, 'control_panel/meal_log_list.html', {
        'meals': meals
    })


@admin_required
def add_meal_log(request):
    form = MealLogForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('meal_log_list')

    return render(request, 'control_panel/meal_log_form.html', {'form': form})


@admin_required
def edit_meal_log(request, id):
    meal = get_object_or_404(MealLog, id=id)

    form = MealLogForm(request.POST or None, instance=meal)

    if form.is_valid():
        form.save()
        return redirect('meal_log_list')

    return render(request, 'control_panel/meal_log_form.html', {'form': form})


@admin_required
def delete_meal_log(request, id):
    meal = get_object_or_404(MealLog, id=id)
    meal.delete()

    return redirect('meal_log_list')

from django.http import JsonResponse
from django.template.loader import render_to_string

@admin_required
def food_list(request):
    query = request.GET.get('q', '')

    foods = Food.objects.prefetch_related('categories').order_by('-id')

    if query:
        foods = foods.filter(name__icontains=query)

    # 🔥 AJAX RESPONSE
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            'control_panel/partials/food_list_items.html',
            {'foods': foods}
        )
        return JsonResponse({'html': html})

    return render(request, 'control_panel/food_list.html', {
        'foods': foods
    })


@admin_required
def add_food(request):

    if request.method == 'POST':
        data = request.POST.copy()

        # 🔥 FIX CATEGORY FORMAT
        categories = data.get('categories', '')
        if categories:
            data.setlist('categories', categories.split(','))

        form = FoodForm(data, request.FILES)

        if form.is_valid():
            food = form.save(commit=False)
            food.created_by = request.user
            food.save()
            form.save_m2m()  # now works correctly

            messages.success(request, "Food added successfully ✅")
            return redirect('food_list')

        else:
            print(form.errors)

    else:
        form = FoodForm()

    return render(request, 'control_panel/food_form.html', {'form': form})

@admin_required
def edit_food(request, id):
    food = get_object_or_404(Food, id=id)

    if request.method == 'POST':
        data = request.POST.copy()

        categories = data.get('categories', '')
        if categories:
            data.setlist('categories', categories.split(','))

        form = FoodForm(data, request.FILES, instance=food)

        if form.is_valid():
            food = form.save()
            messages.success(request, "Food updated ✨")
            return redirect('food_list')

        else:
            print(form.errors)

    else:
        form = FoodForm(instance=food)

    return render(request, 'control_panel/food_form.html', {'form': form})

@admin_required
def delete_food(request, id):
    food = get_object_or_404(Food, id=id)
    food.delete()

    return redirect('food_list')

@admin_required
def recipe_list(request):

    recipes = Recipe.objects.select_related('category').order_by('-id')

    query = request.GET.get('q')

    if query:
        recipes = recipes.filter(name__icontains=query)

    # 🔥 AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        html = render_to_string(
            'control_panel/partials/recipe_items.html',
            {'recipes': recipes},
            request=request
        )

        return JsonResponse({
            'html': html,
            'count': recipes.count()
        })

    return render(request, 'control_panel/recipe_list.html', {
        'recipes': recipes
    })


@admin_required
def add_recipe(request):
    form = RecipeForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('recipe_list')

    return render(request, 'control_panel/recipe_form.html', {'form': form})


@admin_required
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)

    if form.is_valid():
        form.save()
        return redirect('recipe_list')

    return render(request, 'control_panel/recipe_form.html', {'form': form})


@admin_required
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe.delete()

    return redirect('recipe_list')

@admin_required
def recipe_category_list(request):
    categories = RecipeCategory.objects.all().order_by('-id')

    return render(request, 'control_panel/recipe_category_list.html', {
        'categories': categories
    })


@admin_required
def add_recipe_category(request):
    form = RecipeCategoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('recipe_category_list')

    return render(request, 'control_panel/recipe_category_form.html', {'form': form})


@admin_required
def edit_recipe_category(request, id):
    category = get_object_or_404(RecipeCategory, id=id)

    form = RecipeCategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        form.save()
        return redirect('recipe_category_list')

    return render(request, 'control_panel/recipe_category_form.html', {'form': form})


@admin_required
def delete_recipe_category(request, id):
    category = get_object_or_404(RecipeCategory, id=id)
    category.delete()

    return redirect('recipe_category_list')


@admin_required
def user_list(request):
    users = User.objects.all().order_by('-id')

    q = request.GET.get('q')
    if q:
        users = users.filter(username__icontains=q)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'is_staff': u.is_staff
            }
            for u in users
        ]
        return JsonResponse({'users': data})

    return render(request, 'control_panel/user_list.html', {
        'users': users
    })


@admin_required
def add_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = True if request.POST.get('is_staff') else False

        # 🔥 prevent duplicate usernames
        if User.objects.filter(username=username).exists():
            return render(request, 'control_panel/add_user.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_staff = is_staff
        user.save()

        return redirect('user_list')

    return render(request, 'control_panel/add_user.html')

@admin_required
def edit_user(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        # 🔥 ADMIN TOGGLE
        user.is_staff = True if request.POST.get('is_staff') else False

        user.save()
        return redirect('user_list')

    return render(request, 'control_panel/user_form.html', {
        'user_obj': user
    })

@admin_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()

    return redirect('user_list')

@admin_required
def profile_list(request):
    profiles = Profile.objects.select_related('user').all()

    return render(request, 'control_panel/profile_list.html', {
        'profiles': profiles
    })

@admin_required
def get_profile_data(request):
    user_id = request.GET.get('user_id')

    try:
        profile = Profile.objects.get(user_id=user_id)

        data = {
            'height': profile.height,
            'weight': profile.weight,
            'start_weight': profile.start_weight,
            'target_weight': profile.target_weight,
            'daily_steps_target': profile.daily_steps_target,
            'daily_calorie_target': profile.daily_calorie_target,
            'daily_protein_target': profile.daily_protein_target,
            'max_cheat_calories': profile.max_cheat_calories,
            'max_cheat_meals': profile.max_cheat_meals,
            'goal': profile.goal,
            'points': profile.points,
            'daily_water_goal': profile.daily_water_goal,
            'is_onboarded': profile.is_onboarded,
        }

        return JsonResponse({'exists': True, 'data': data})

    except Profile.DoesNotExist:
        return JsonResponse({'exists': False})

@admin_required
def add_profile(request):
    form = ProfileForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('profile_list')

    return render(request, 'control_panel/profile_form.html', {'form': form})

@admin_required
def edit_profile(request, id):
    profile = get_object_or_404(Profile, id=id)

    form = ProfileForm(request.POST or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect('profile_list')

    return render(request, 'control_panel/profile_form.html', {'form': form})

@admin_required
def delete_profile(request, id):
    profile = get_object_or_404(Profile, id=id)
    profile.delete()

    return redirect('profile_list')

@admin_required
def muscle_group_list(request):
    groups = MuscleGroup.objects.all()

    return render(request, 'control_panel/muscle_group_list.html', {
        'groups': groups
    })

@admin_required
def add_muscle_group(request):
    from .forms import MuscleGroupForm
    form = MuscleGroupForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('muscle_group_list')

    return render(request, 'control_panel/muscle_group_form.html', {'form': form})


@admin_required
def edit_muscle_group(request, id):
    from .forms import MuscleGroupForm
    group = get_object_or_404(MuscleGroup, id=id)

    form = MuscleGroupForm(request.POST or None, instance=group)

    if form.is_valid():
        form.save()
        return redirect('muscle_group_list')

    return render(request, 'control_panel/muscle_group_form.html', {'form': form})


@admin_required
def delete_muscle_group(request, id):
    group = get_object_or_404(MuscleGroup, id=id)
    group.delete()

    return redirect('muscle_group_list')


@admin_required
def sub_muscle_list(request):
    subs = SubMuscle.objects.select_related('muscle_group').all()

    return render(request, 'control_panel/sub_muscle_list.html', {
        'subs': subs
    })

@admin_required
def add_sub_muscle(request):
    from .forms import SubMuscleForm
    form = SubMuscleForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('sub_muscle_list')

    return render(request, 'control_panel/sub_muscle_form.html', {'form': form})


@admin_required
def edit_sub_muscle(request, id):
    from .forms import SubMuscleForm
    sub = get_object_or_404(SubMuscle, id=id)

    form = SubMuscleForm(request.POST or None, instance=sub)

    if form.is_valid():
        form.save()
        return redirect('sub_muscle_list')

    return render(request, 'control_panel/sub_muscle_form.html', {'form': form})


@admin_required
def delete_sub_muscle(request, id):
    sub = get_object_or_404(SubMuscle, id=id)
    sub.delete()

    return redirect('sub_muscle_list')