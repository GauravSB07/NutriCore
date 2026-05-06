from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # 📚 WORKOUT LIBRARY (INFO)
    # =========================
    path('library/', views.workout_library, name='workout_library'),
    path('library/<int:muscle_id>/', views.sub_muscle_list, name='sub_muscle_list'),
    path('library/sub/<int:sub_id>/', views.exercise_list, name='exercise_list'),
    path('library/exercise/<int:id>/', views.exercise_detail, name='exercise_detail'),


    # =========================
    # 💪 START WORKOUT FLOW
    # =========================
    path('start/', views.start_workout, name='start_workout'),

    # Step 1 → choose muscle
    path('start/<int:muscle_id>/', views.choose_submuscle, name='choose_sub'),

    # Step 2 → choose sub muscle (start session)
    path('start/sub/<int:sub_id>/', views.choose_exercise, name='choose_exercise'),

    # Step 3 → log sets
    path('log/<int:session_id>/', views.log_sets, name='log_sets'),
]