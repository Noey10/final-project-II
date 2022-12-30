from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('information', views.information, name='information'),
    path('homepage', views.homepage, name='homepage'),    
      
]