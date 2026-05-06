from django.urls import path
from .views import signup_view,login_view,profile_view,edit_profile,welcome_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/',signup_view,name='signup'),
    path('login/',login_view,name ='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('welcome/', welcome_view, name='welcome'),
]
