from django.urls import path, include
from . import views


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register", view=views.register, name="register"),
    path('profile', views.show_profile, name='profile'),
    path('update_profile', views.update_profile, name='update_profile'), 
    path('my_history', views.my_history, name='my_history'),
    path('my_dashboard', views.my_dashboard, name='my_dashboard'),
    path('history_item/<int:id>', views.history_item, name='history_item'),
    path('add_teacher', views.add_teacher, name='add_teacher'),
    path('view_teacher', views.view_teacher, name='view_teacher'),
    path('update_teacher/<str:id>', views.update_teacher, name="update_teacher"),
    path('delete_teacher/<str:id>', views.delete_teacher, name='delete_teacher'),
]
