from django.urls import path
from . import views

urlpatterns = [
    #test upload model course
    path('test_upload', views.test_upload, name="test_upload"), 
    path('show_data_course', views.show_data_course, name="show_data_course"), 
    
    
    

    
]