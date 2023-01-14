from django.urls import path, include
from . import views


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register", view=views.register, name="register"),
    path('profile', views.profile, name='profile'), 
    path('my-dashboard', views.my_dashboard, name='my-dashboard'),
]
