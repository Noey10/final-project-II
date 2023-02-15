from django.urls import path
from . import views

urlpatterns = [
    #upload model
    path('upload', views.upload_model, name='upload'),
    path('upload_sci_model', views.upload_sci_model, name='upload_sci_model'),
    #Applied science model
    path('data_in_applied_sci', views.data_in_applied_sci, name="data_in_applied_sci"),
    path('delete_data_applied', views.delete_data_applied, name="delete_data_applied"),
    #Health science model
    path('data_in_health_sci', views.data_in_health_sci, name="data_in_health_sci"),
    path('delete_data_health', views.delete_data_health, name="delete_data_health"),
    #Pure science model
    path('data_in_pure_sci', views.data_in_pure_sci, name="data_in_pure_sci"),
    path('delete_data_pure', views.delete_data_pure, name="delete_data_pure"),
    #show button select model
    path('show_model', views.show_model, name="show_model"),    
    #delete all data all model
    path('delete_all_data', views.delete_all_data, name="delete_all_data"), 
    
    #test upload model course
    path('test_upload', views.test_upload, name="test_upload"), 
    path('add_major', views.add_major, name="add_major"), 
    path('show_data_course', views.show_data_course, name="show_data_course"), 
    
    
    

    
]