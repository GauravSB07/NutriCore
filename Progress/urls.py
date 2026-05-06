from django.urls import path
from .views import daily_report, weekly_report, monthly_report, workout_progress,workout_reports,workout_charts,log_steps

urlpatterns = [
    path('daily/', daily_report, name='daily_report'),
    path('weekly/', weekly_report, name='weekly_report'),
    path('monthly/', monthly_report, name='monthly_report'),
    path('workout/', workout_progress, name='workout_progress'),
    path('workout-reports/', workout_reports, name='workout_reports'),
    path('workout-charts/', workout_charts, name='workout_charts'),
    path('steps/', log_steps, name='log_steps'),
]
