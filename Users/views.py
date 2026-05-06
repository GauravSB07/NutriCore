from django.shortcuts import render,redirect
from .forms import SignupForm,ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.timezone import localdate
from django.db.models import Sum
from Nutrition.models import MealLog,WaterIntake
from django.contrib.auth.decorators import login_required
from Progress.models import StepsLog

# Create your views here.

@login_required
def welcome_view(request):
    if request.user.profile.is_onboarded:
        return redirect('home')
    return render(request, 'users/welcome.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('welcome')
    else:
        form = SignupForm()

    return render(request,'users/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # 🔥 FIX: CHECK ADMIN
            if user.is_superuser:   # or user.is_staff
                return redirect('admin_dashboard')
            else:
                return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def home_view(request):

    # 🔥 FIRST CHECK LOGIN
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user

    # 🔥 SAFE PROFILE
    profile = getattr(user, 'profile', None)

    if not profile:
        return redirect('welcome')

    # 🔥 ONBOARDING CHECK
    if not profile.is_onboarded:
        return redirect('welcome')

    today = localdate()

    meals = MealLog.objects.filter(
        user=user,
        date=today
    )

    total_calories = (
        meals.aggregate(Sum('calories'))['calories__sum']
        or 0
    )

    total_protein = (
        meals.aggregate(Sum('protein'))['protein__sum']
        or 0
    )

    # 🔥 CHEAT DATA
    cheat_meals = meals.filter(is_cheat=True)

    cheat_calories = (
        cheat_meals.aggregate(Sum('calories'))['calories__sum']
        or 0
    )

    cheat_count = cheat_meals.count()

    # 🔥 WATER
    water_today = WaterIntake.objects.filter(
        user=user,
        date=today
    )

    total_water = (
        water_today.aggregate(Sum('amount'))['amount__sum']
        or 0
    )

    # 🔥 DAY STATUS
    if profile.goal == 'cut':

        if total_calories <= profile.daily_calorie_target:
            day_type = "Good (Fat Loss)"
        else:
            day_type = "Overeaten"

    else:

        if total_calories >= profile.daily_calorie_target:
            day_type = "Good (Bulk)"
        else:
            day_type = "Undereaten"

    # 🔥 STEPS
    steps_today = StepsLog.objects.filter(
        user=user,
        date=today
    )

    total_steps = (
        steps_today.aggregate(Sum('steps'))['steps__sum']
        or 0
    )

    goal = profile.daily_steps_target or 8000

    steps_remaining = max(goal - total_steps, 0)

    steps_percent = min(
        (total_steps / goal) * 100,
        100
    )

    return render(request, 'home.html', {

        'total_calories': total_calories,
        'total_protein': total_protein,

        'cheat_calories': cheat_calories,
        'cheat_count': cheat_count,

        'day_type': day_type,

        'total_water': total_water,

        'profile': profile,

        'total_steps': total_steps,
        'steps_remaining': steps_remaining,
        'steps_percent': steps_percent,

    })

# 🔥 PROFILE VIEW
@login_required
def profile_view(request):
    profile = request.user.profile

    # 🔥 WEIGHT PROGRESS (MAIN LOGIC)
    weight_progress = 0

    if profile.start_weight and profile.target_weight and profile.weight:
        total = abs(profile.start_weight - profile.target_weight)
        done = abs(profile.start_weight - profile.weight)

        if total != 0:
            weight_progress = (done / total) * 100

    return render(request, 'users/profile.html', {
        'profile': profile,
        'weight_progress': min(weight_progress, 100)
    })


# 🔥 EDIT PROFILE VIEW
@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':

        # 🔹 BASIC INFO
        profile.goal = request.POST.get('goal')

        # 🔹 BODY
        profile.height = float(request.POST.get('height') or 0)
        profile.weight = float(request.POST.get('weight') or 0)
        profile.start_weight = float(request.POST.get('start_weight') or 0)
        profile.target_weight = float(request.POST.get('target_weight') or 0)

        # 🔹 TARGETS
        profile.daily_calorie_target = float(request.POST.get('daily_calorie_target') or 0)
        profile.daily_protein_target = float(request.POST.get('daily_protein_target') or 0)
        profile.daily_steps_target = int(request.POST.get('daily_steps_target') or 0)

        # 🔹 IMAGE
        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']

        profile.is_onboarded = True
        profile.save()

        return redirect('profile')

    return render(request, 'users/edit_profile.html', {
        'profile': profile
    })