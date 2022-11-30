from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('information', views.information, name='information'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='profile'),    
]