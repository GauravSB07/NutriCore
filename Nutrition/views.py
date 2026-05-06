from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now, localdate
from django.db.models import Sum
from datetime import timedelta
from django.urls import reverse
from django.http import HttpResponseRedirect,JsonResponse
from .forms import MealLogForm
from .models import MealLog, Food,WaterIntake,Category
from django.db.models import Sum
import math

@login_required
def log_meal(request):
    profile = request.user.profile
    today = localdate()

    if request.method == "POST":
        form = MealLogForm(request.POST)

        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user

            food = meal.food
            quantity = float(meal.quantity)
            unit = request.POST.get('unit')

            # 🔥 CONVERT SERVING → BASE UNIT
            if unit == 'serving' and food.serving_quantity:
                quantity = quantity * food.serving_quantity
                unit = food.unit_type  # convert to base

            # 🔹 Calculate calories + protein
            if unit in ['g', 'ml']:
                meal.calories = (food.calories_per_100g / 100) * quantity
                meal.protein = (food.protein_per_100g / 100) * quantity if food.protein_per_100g else 0

            else:  # unit (pieces)
                meal.calories = food.calories_per_unit * quantity
                meal.protein = food.protein_per_unit * quantity if food.protein_per_unit else 0

            # 🔥 Cheat logic
            is_cheat = request.POST.get('is_cheat') == 'on'
            meal.is_cheat = is_cheat

            if is_cheat:
                required_points = int(meal.calories / 4)

                if profile.points < required_points:
                    messages.error(request, "Not enough points!")
                    return redirect('nutrition:log_meal')

                today_cheat_calories = MealLog.objects.filter(
                    user=request.user,
                    date=today,
                    is_cheat=True
                ).aggregate(Sum('calories'))['calories__sum'] or 0

                if today_cheat_calories + meal.calories > profile.max_cheat_calories_per_day:
                    messages.error(request, "Daily cheat calorie limit exceeded!")
                    return redirect('nutrition:log_meal')

                today_cheat_count = MealLog.objects.filter(
                    user=request.user,
                    date=today,
                    is_cheat=True
                ).count()

                if today_cheat_count >= profile.max_cheat_meals_per_day:
                    messages.error(request, "Max cheat meals reached!")
                    return redirect('nutrition:log_meal')

                profile.points -= required_points
                profile.save()

            meal.save()

            messages.success(request, "Meal logged successfully!")
            return redirect('nutrition:meal_list')

    else:
        form = MealLogForm()

    return render(request, 'nutrition/log_meal.html', {'form': form})


@login_required
def meal_list(request):

    user = request.user

    today = localdate()

    meals = MealLog.objects.filter(
        user=user,
        date=today
    ).order_by('-id')

    totals = meals.aggregate(

        total_calories=Sum('calories'),

        total_protein=Sum('protein')

    )

    total_calories = (
        totals['total_calories'] or 0
    )

    total_protein = (
        totals['total_protein'] or 0
    )

    # 🔥 TARGET
    target_calories = getattr(
        user.profile,
        'daily_calories',
        2000
    )

    # 🔥 PROGRESS %
    if target_calories > 0:

        percent = min(
            total_calories / target_calories,
            1
        )

    else:

        percent = 0

    # 🔥 SVG CIRCLE
    radius = 26

    circumference = (
        2 * math.pi * radius
    )

    calories_offset = (
        circumference * (1 - percent)
    )

    return render(
        request,
        'nutrition/meal_list.html',
        {

            'meals': meals,

            'total_calories': total_calories,

            'total_protein': total_protein,

            'target_calories': target_calories,

            'calories_offset': calories_offset,

        }
    )


# 🔥 DELETE MEAL
@login_required
def delete_meal(request, id):
    meal = get_object_or_404(MealLog, id=id, user=request.user)
    meal.delete()
    messages.success(request, "Meal deleted")
    return redirect('nutrition:meal_list')


# 🔥 EDIT MEAL
@login_required
def edit_meal(request, id):
    meal = get_object_or_404(MealLog, id=id, user=request.user)

    if request.method == 'POST':
        form = MealLogForm(request.POST, instance=meal)

        if form.is_valid():
            updated = form.save(commit=False)

            food = updated.food
            quantity = updated.quantity
            unit = updated.unit

            # 🔥 HANDLE SERVING ALSO (important fix)
            if unit == 'serving' and food.serving_quantity:
                quantity = quantity * food.serving_quantity
                unit = food.unit_type

            # 🔥 CALCULATION
            if unit in ['g', 'ml']:
                updated.calories = (food.calories_per_100g / 100) * quantity
                updated.protein = (food.protein_per_100g / 100) * quantity if food.protein_per_100g else 0
            else:
                updated.calories = food.calories_per_unit * quantity
                updated.protein = food.protein_per_unit * quantity if food.protein_per_unit else 0

            updated.save()
            messages.success(request, "Meal Updated")
            return redirect('nutrition:meal_list')

    else:
        form = MealLogForm(instance=meal)

    # 🔥 IMPORTANT: SEND edit_meal
    return render(request, 'nutrition/log_meal.html', {
        'form': form,
        'edit_meal': meal   # ✅ THIS FIXES PREFILL
    })


def food_list(request):
    category_ids = request.GET.getlist('category')

    foods = Food.objects.all()

    if category_ids:
        foods = foods.filter(categories__id__in=category_ids).distinct()

    categories = Category.objects.all()

    return render(request, 'nutrition/food_list.html', {
        'foods': foods,
        'categories': categories,
        'selected_categories': category_ids   
    })

@login_required
def food_detail(request, id):

    food = get_object_or_404(Food, id=id)

    if request.method == 'POST':

        quantity = float(
            request.POST.get('quantity') or 0
        )

        cal100 = food.calories_per_100g or 0
        prot100 = food.protein_per_100g or 0

        calUnit = food.calories_per_unit or 0
        protUnit = food.protein_per_unit or 0

        # 🔥 CALCULATION
        if food.unit_type in ['g', 'ml']:

            calories = (cal100 / 100) * quantity

            protein = (prot100 / 100) * quantity

        else:

            calories = calUnit * quantity

            protein = protUnit * quantity

        # 🔥 CREATE MEAL
        MealLog.objects.create(

            user=request.user,

            food=food,

            quantity=quantity,

            calories=calories,

            protein=protein

        )

        messages.success(
            request,
            "Meal Added Successfully ✅"
        )

        return redirect('nutrition:meal_list')

    return render(
        request,
        'nutrition/food_detail.html',
        {
            'food': food
        }
    )


@login_required
def add_cheat_meal(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    profile = request.user.profile
    today = localdate()

    if request.method == 'POST':
        quantity = float(request.POST.get('quantity') or 0)

        if quantity <= 0:
            messages.error(request, "Enter valid quantity")
            return redirect('nutrition:add_cheat_meal', food_id=food.id)

        # 🔥 CALCULATE
        if food.unit_type in ['g', 'ml']:
            calories = (food.calories_per_100g or 0) / 100 * quantity
            protein = (food.protein_per_100g or 0) / 100 * quantity
        else:
            calories = (food.calories_per_unit or 0) * quantity
            protein = (food.protein_per_unit or 0) * quantity

        required_points = int(calories / 4)

        # 🔴 VALIDATIONS
        if profile.points < required_points:
            messages.error(request, f"Not enough points! Need {required_points}")
            return redirect('nutrition:add_cheat_meal', food_id=food.id)

        today_cheat_calories = MealLog.objects.filter(
            user=request.user,
            date=today,
            is_cheat=True
        ).aggregate(Sum('calories'))['calories__sum'] or 0

        if today_cheat_calories + calories > profile.max_cheat_calories_per_day:
            messages.error(request, "Cheat calorie limit exceeded!")
            return redirect('nutrition:add_cheat_meal', food_id=food.id)

        today_cheat_count = MealLog.objects.filter(
            user=request.user,
            date=today,
            is_cheat=True
        ).count()

        if today_cheat_count >= profile.max_cheat_meals_per_day:
            messages.error(request, "Max cheat meals reached!")
            return redirect('nutrition:add_cheat_meal', food_id=food.id)

        # ✅ SAVE MEAL
        MealLog.objects.create(
            user=request.user,
            food=food,
            quantity=quantity,
            unit=food.unit_type,
            is_cheat=True
        )

        # ✅ DEDUCT POINTS
        profile.points -= required_points
        profile.save()

        messages.success(request, f"🔥 Cheat meal added (-{required_points} pts)")
        return redirect('nutrition:meal_list')

    return render(request, 'nutrition/cheat_meal.html', {'food': food})


@login_required
def log_water(request):

    today = localdate()   # ✅ FIX (IMPORTANT)
    profile = request.user.profile

    if request.method == 'POST':
        amount = request.POST.get('amount')

        if amount:
            WaterIntake.objects.create(
                user=request.user,
                amount=float(amount),
                date=today   # ✅ ENSURE CORRECT DATE
            )
            messages.success(request, f"+{amount} ml added")

        return redirect('nutrition:log_water')

    # 🔥 ONLY TODAY'S WATER
    water_today = WaterIntake.objects.filter(
        user=request.user,
        date=today
    )

    total_water = water_today.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    # 🔥 PROGRESS
    goal = profile.daily_water_goal or 3000

    progress_percent = (total_water / goal) * 100 if goal else 0

    return render(request, 'nutrition/log_water.html', {
        'total_water': total_water,
        'goal': goal,
        'progress_percent': min(progress_percent, 100)
    })