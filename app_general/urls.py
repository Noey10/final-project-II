from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('information', views.information, name='information'),
    path('profile', views.profile, name='profile'),  
    path('homepage', views.homepage, name='homepage'),    
      
]