from django.urls import path, include
from . import views


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register", view=views.register, name="register"),
    path('profile', views.profile, name='profile'), 
    path('my_history', views.my_history, name='my_history'),
    path('my_dashboard', views.my_dashboard, name='my_dashboard'),
    path('update_predict/<int:id>', views.update_predict, name='update_predict'),
    
    
]
