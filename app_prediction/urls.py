from django.urls import path
from . import views

urlpatterns = [
    path('form', views.form, name='form'),
    path('information', views.information, name='information'),
    path('result', views.result, name='result'),
    
]