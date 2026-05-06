from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
from Nutrition.models import MealLog
from Workouts.models import WorkoutSet,WorkoutSession,SubMuscle
from collections import defaultdict
from django.utils import timezone
from django.utils.timezone import localdate
from .models import StepsLog
from django.contrib import messages
import math

@login_required
def daily_report(request):
    today = localdate()
    user = request.user
    profile = user.profile

    meals = MealLog.objects.filter(user=user, date=today)

    total_calories = meals.aggregate(Sum('calories'))['calories__sum'] or 0
    total_protein = meals.aggregate(Sum('protein'))['protein__sum'] or 0

    calories_left = profile.daily_calorie_target - total_calories
    protein_left = profile.daily_protein_target - total_protein

    if profile.goal == 'cut':
        if total_calories <= profile.daily_calorie_target:
            day_type = "Good (Fat Loss)"
            good_day = True
        else:
            day_type = "Overeaten"
            good_day = False
    else:
        if total_calories >= profile.daily_calorie_target:
            day_type = "Good (Bulk)"
            good_day = True
        else:
            day_type = "Undereaten"
            good_day = False

    if good_day:
        last_rewarded = request.session.get('last_rewarded_date')

        if last_rewarded != str(today):
            profile.points += 50
            profile.save()

            request.session['last_rewarded_date'] = str(today)

    
    steps_today = StepsLog.objects.filter(
        user=request.user,
        date=today
    )

    total_steps = steps_today.aggregate(
        Sum('steps')
    )['steps__sum'] or 0

    goal = request.user.profile.daily_steps_target or 8000

    steps_left = max(goal - total_steps, 0)
    steps_percent = (total_steps / goal) * 100 if goal else 0

    

    return render(request, 'progress/daily_report.html', {
        'total_calories': total_calories,
        'total_protein': total_protein,
        'calories_left': calories_left,
        'protein_left': protein_left,
        'day_type': day_type,
        'points': profile.points,
        'steps': total_steps,
        'steps_left': steps_left,
        'steps_percent': min(steps_percent, 100)
    })

@login_required
def weekly_report(request):
    today = now().date()
    profile = request.user.profile

    labels = []
    calories_data = []
    protein_data = []
    cheat_days = []

    total_progress = 0

    for i in range(7):
        day = today - timedelta(days=i)

        meals = MealLog.objects.filter(user=request.user, date=day)

        total_calories = meals.aggregate(Sum('calories'))['calories__sum'] or 0
        total_protein = meals.aggregate(Sum('protein'))['protein__sum'] or 0
        is_cheat_day = meals.filter(is_cheat=True).exists()

        # 🔥 Better label (Mon, Tue...)
        labels.append(day.strftime('%a'))

        calories_data.append(total_calories)
        protein_data.append(total_protein)
        cheat_days.append(is_cheat_day)

        # 🔥 Daily progress capped at 100
        if profile.daily_calorie_target:
            total_progress += min(total_calories / profile.daily_calorie_target, 1)

    # reverse
    labels.reverse()
    calories_data.reverse()
    protein_data.reverse()
    cheat_days.reverse()

    # 🔥 REAL PROGRESS (avg of daily completion)
    progress_percent = (total_progress / 7) * 100 if profile.daily_calorie_target else 0

    radius = 40
    circumference = 2 * math.pi * radius 

    percent = progress_percent / 100
    ring_offset = circumference * (1 - percent)

    # 🔥 STRICT STREAK (no cheat + full target)
    streak = 0
    for i in range(6, -1, -1):
        if calories_data[i] >= profile.daily_calorie_target and not cheat_days[i]:
            streak += 1
        else:
            break

    return render(request, 'progress/weekly_report.html', {
        'labels': labels,
        'calories': calories_data,
        'protein': protein_data,
        'cheat_days': cheat_days,
        'target_calories': profile.daily_calorie_target,
        'progress_percent': round(progress_percent, 1),
        'streak': streak,
        'ring_offset': ring_offset,
    })

@login_required
def monthly_report(request):
    user = request.user
    profile = user.profile

    today = timezone.now().date()
    start_date = today - timedelta(days=27)

    meals = MealLog.objects.filter(user=user, date__gte=start_date)

    # =========================
    # 🔥 GROUP BY DAY
    # =========================
    daily_data = defaultdict(lambda: {'calories': 0, 'protein': 0, 'cheat': False})

    for m in meals:
        d = m.date
        daily_data[d]['calories'] += m.calories
        daily_data[d]['protein'] += m.protein
        if m.is_cheat:
            daily_data[d]['cheat'] = True

    # =========================
    # 📊 DAILY LIST
    # =========================
    all_days = []
    labels, calories, protein = [], [], []

    for i in range(28):
        day = start_date + timedelta(days=i)
        data = daily_data.get(day, {'calories': 0, 'protein': 0, 'cheat': False})

        all_days.append(data)
        labels.append(day.strftime("%d"))
        calories.append(data['calories'])
        protein.append(data['protein'])

    # =========================
    # 🔥 WEEKLY SUMMARY
    # =========================
    weekly_summary = []

    total_fat_loss_days = 0
    total_cheat_days = 0

    for i in range(4):
        week = all_days[i*7:(i+1)*7]

        avg_cal = sum(d['calories'] for d in week) // 7
        avg_pro = sum(d['protein'] for d in week) // 7

        cheat_days = sum(1 for d in week if d['cheat'])
        fat_loss_days = sum(
            1 for d in week
            if d['calories'] <= profile.daily_calorie_target
        )

        # 🔥 accumulate totals (IMPORTANT)
        total_cheat_days += cheat_days
        total_fat_loss_days += fat_loss_days

        weekly_summary.append({
            'week': f"Week {i+1}",
            'avg_calories': avg_cal,
            'avg_protein': avg_pro,
            'cheat_days': cheat_days,
            'fat_loss_days': fat_loss_days
        })

    # =========================
    # 🔥 CONSISTENCY (FIXED)
    # =========================
    consistency_days = total_fat_loss_days

    # =========================
    # 🔥 PROGRESS
    # =========================
    progress = int((consistency_days / 28) * 100)

    # =========================
    # 🔥 STREAK
    # =========================
    streak = 0
    for d in reversed(all_days):
        if d['calories'] <= profile.daily_calorie_target and not d['cheat']:
            streak += 1
        else:
            break

    return render(request, 'progress/monthly_report.html', {
        'weekly_summary': weekly_summary,
        'labels': labels,
        'calories': calories,
        'protein': protein,
        'target_calories': profile.daily_calorie_target,

        # 🔥 FIXED VALUES
        'consistency_days': consistency_days,
        'cheat_days': total_cheat_days,
        'progress': progress,
        'streak': streak
    })


@login_required
def workout_progress(request):
    user = request.user

    sets = WorkoutSet.objects.filter(
        session__user=user
    ).select_related(
        'exercise',
        'session__sub_muscle__muscle_group'
    ).order_by('session__date')

    data = defaultdict(lambda: defaultdict(list))

    # 🔥 GROUP DATA
    for s in sets:
        muscle = s.session.sub_muscle.muscle_group.name
        exercise = s.exercise.name

        data[muscle][exercise].append({
            'weight': s.weight,
            'date': s.session.date
        })

    # 🔥 ANALYZE PROGRESS
    final_data = {}

    for muscle, exercises in data.items():
        final_data[muscle] = []

        for exercise, records in exercises.items():
            weights = [r['weight'] for r in records]

            improved = False
            if len(weights) >= 2:
                improved = weights[-1] > weights[0]

            final_data[muscle].append({
                'name': exercise,
                'records': records[-5:],  # last 5
                'improved': improved
            })

    return render(request, 'progress/workout_progress.html', {
        'data': final_data
    })

from datetime import timedelta
from django.utils.timezone import now
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Workouts.models import WorkoutSession, SubMuscle


@login_required
def workout_reports(request):
    user = request.user

    week_offset = int(request.GET.get('week', 0))
    today = now().date()

    # 🔥 WEEK RANGE
    start_of_week = today - timedelta(days=today.weekday()) - timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)

    prev_start = start_of_week - timedelta(days=7)
    prev_end = start_of_week - timedelta(days=1)

    # 🔥 QUERY
    sessions = WorkoutSession.objects.filter(
        user=user,
        date__range=(start_of_week, end_of_week)
    ).select_related('sub_muscle__muscle_group')

    prev_sessions = WorkoutSession.objects.filter(
        user=user,
        date__range=(prev_start, prev_end)
    ).select_related('sub_muscle__muscle_group')

    muscle_counts = defaultdict(int)
    sub_counts = defaultdict(int)
    prev_counts = defaultdict(int)
    prev_sub_counts = defaultdict(int)
    muscle_sub_map = defaultdict(set)

    # 🔥 CURRENT WEEK
    for s in sessions:
        muscle = s.sub_muscle.muscle_group.name
        sub = s.sub_muscle.name

        muscle_counts[muscle] += 1
        sub_counts[sub] += 1
        muscle_sub_map[muscle].add(sub)

    # 🔥 PREVIOUS WEEK
    for s in prev_sessions:
        muscle = s.sub_muscle.muscle_group.name
        sub = s.sub_muscle.name

        prev_counts[muscle] += 1
        prev_sub_counts[sub] += 1

    # 🔥 MUSCLE REPORT
    report = []
    all_muscles = set(list(muscle_counts.keys()) + list(prev_counts.keys()))

    for muscle in all_muscles:
        current = muscle_counts[muscle]
        prev = prev_counts.get(muscle, 0)

        report.append({
            'muscle': muscle,
            'current': current,
            'prev': prev,
            'change': current - prev
        })

    # 🔥 SUB MUSCLE REPORT
    sub_report = []
    all_subs = set(list(sub_counts.keys()) + list(prev_sub_counts.keys()))

    for sub in all_subs:
        current = sub_counts[sub]
        prev = prev_sub_counts.get(sub, 0)

        sub_report.append({
            'sub': sub,
            'current': current,
            'prev': prev,
            'change': current - prev
        })

    # 🔥 BALANCE
    imbalance = {}

    for muscle in muscle_sub_map:
        all_subs_db = SubMuscle.objects.filter(muscle_group__name=muscle)
        trained_subs = muscle_sub_map[muscle]

        missing = [s.name for s in all_subs_db if s.name not in trained_subs]

        imbalance[muscle] = {
            'missing': missing,
            'balance_score': int((len(trained_subs) / len(all_subs_db)) * 100) if all_subs_db else 0
        }

    context = {
        'report': report,
        'sub_report': sub_report,
        'imbalance': imbalance,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'week_offset': week_offset
    }

    return render(request, 'progress/workout_reports.html', context)


@login_required
def workout_charts(request):
    user = request.user

    week_offset = int(request.GET.get('week', 0))

    today = now().date()

    start_of_week = today - timedelta(days=today.weekday()) - timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)

    sets = WorkoutSet.objects.filter(
        session__user=user,
        session__date__range=(start_of_week, end_of_week)
    ).select_related('exercise', 'session__sub_muscle__muscle_group')

    from collections import defaultdict

    exercise_data = defaultdict(list)
    muscle_counts = defaultdict(int)

    counted_sessions = set()

    for s in sets:
        exercise_data[s.exercise.name].append({
            'date': str(s.session.date),
            'weight': s.weight
        })

        # count muscle once per session
        if s.session.id not in counted_sessions:
            counted_sessions.add(s.session.id)
            muscle = s.session.sub_muscle.muscle_group.name
            muscle_counts[muscle] += 1

    context = {
        'exercise_data': dict(exercise_data),
        'muscle_counts': dict(muscle_counts),
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'week_offset': week_offset
    }

    return render(request, 'progress/workout_charts.html', context)

@login_required
def log_steps(request):

    today = localdate()
    profile = request.user.profile

    if request.method == "POST":
        steps = request.POST.get("steps")

        if steps:
            StepsLog.objects.create(
                user=request.user,
                steps=int(steps),
                date=today
            )
            messages.success(request, f"+{steps} steps added")

        return redirect('log_steps')

    # 🔥 TODAY STEPS
    steps_today = StepsLog.objects.filter(
        user=request.user,
        date=today
    )

    total_steps = steps_today.aggregate(
        Sum('steps')
    )['steps__sum'] or 0

    goal = profile.daily_steps_target or 8000
    remaining = max(goal - total_steps, 0)

    progress_percent = (total_steps / goal) * 100 if goal else 0

    return render(request, 'progress/log_steps.html', {
        'total_steps': total_steps,
        'goal': goal,
        'remaining': remaining,
        'progress_percent': min(progress_percent, 100)
    })





















    