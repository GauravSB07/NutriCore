from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exercise, WorkoutSession, WorkoutSet, MuscleGroup, SubMuscle


# =========================
# 🧠 WORKOUT LIBRARY (INFO)
# =========================

# 1️⃣ Muscle List
def workout_library(request):
    muscles = MuscleGroup.objects.all()

    return render(request, 'workouts/muscle_list.html', {
        'muscles': muscles
    })


# 2️⃣ Sub-Muscle List
def sub_muscle_list(request, muscle_id):
    muscle = get_object_or_404(MuscleGroup, id=muscle_id)
    sub_muscles = muscle.sub_muscles.all()

    return render(request, 'workouts/sub_muscle_list.html', {
        'muscle': muscle,
        'sub_muscles': sub_muscles
    })


# 3️⃣ Exercise List
def exercise_list(request, sub_id):
    sub_muscle = get_object_or_404(SubMuscle, id=sub_id)
    exercises = sub_muscle.exercises.all()

    return render(request, 'workouts/exercise_list.html', {
        'sub_muscle': sub_muscle,
        'exercises': exercises
    })


# 4️⃣ Exercise Detail
def exercise_detail(request, id):
    exercise = Exercise.objects.get(id=id)

    # 🔥 FIX: convert '\n' text → real new lines
    if exercise.steps:
        exercise.steps = exercise.steps.replace('\\n', '\n')

    return render(request, 'workouts/exercise_detail.html', {
        'exercise': exercise
    })


# =========================
# 💪 START WORKOUT FLOW
# =========================

# 1️⃣ Select Muscle
@login_required
def start_workout(request):
    muscles = MuscleGroup.objects.all()

    return render(request, 'workouts/start_workout.html', {
        'muscles': muscles
    })


# 2️⃣ Select Sub-Muscle
@login_required
def choose_submuscle(request, muscle_id):
    muscle = get_object_or_404(MuscleGroup, id=muscle_id)
    sub_muscles = muscle.sub_muscles.all()

    return render(request, 'workouts/choose_sub.html', {
        'muscle': muscle,
        'sub_muscles': sub_muscles
    })


# 3️⃣ Start Session (from SubMuscle)
@login_required
def choose_exercise(request, sub_id):
    sub_muscle = get_object_or_404(SubMuscle, id=sub_id)
    exercises = sub_muscle.exercises.all()

    if request.method == 'POST':
        exercise_id = request.POST.get('exercise')

        if not exercise_id:
            return redirect('choose_exercise', sub_id=sub_id)

        # ✅ create session
        session = WorkoutSession.objects.create(
            user=request.user,
            sub_muscle=sub_muscle
        )

        # ✅ store selected exercise
        request.session['selected_exercise'] = exercise_id

        return redirect('log_sets', session_id=session.id)

    return render(request, 'workouts/choose_exercise.html', {
        'sub_muscle': sub_muscle,
        'exercises': exercises
    })


# =========================
# 🏋️ LOG SETS
# =========================

@login_required
def log_sets(request, session_id):
    session = get_object_or_404(WorkoutSession, id=session_id)

    selected_exercise_id = request.session.get('selected_exercise')
    selected_exercise = None

    if selected_exercise_id:
        selected_exercise = Exercise.objects.get(id=selected_exercise_id)

    sets = session.sets.all()

    if request.method == 'POST':
        reps = request.POST.get('reps')
        weight = request.POST.get('weight')

        if not reps or not weight:
            return redirect('log_sets', session_id=session.id)

        count = sets.count() + 1

        WorkoutSet.objects.create(
            session=session,
            exercise=selected_exercise,
            sub_muscle=session.sub_muscle,
            set_number=count,
            reps=int(reps),
            weight=float(weight)
        )

        return redirect('log_sets', session_id=session.id)

    return render(request, 'workouts/log_sets.html', {
        'session': session,
        'exercise': selected_exercise,   
        'sets': sets
    })