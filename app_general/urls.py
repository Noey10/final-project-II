from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),    
    path('error_page', views.error_page, name='error_page'),       

]