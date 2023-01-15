from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_model, name='upload'),
    path('upload_applied_sci_model', views.upload_applied_sci_model, name='upload_applied_sci_model'),
    path('upload_health_sci_model', views.upload_health_sci_model, name='upload_health_sci_model'),
    path('upload_pure_sci_model', views.upload_pure_sci_model, name='upload_pure_sci_model'),
    #Applied science model
    path('data_in_applied_sci', views.data_in_applied_sci, name="data_in_applied_sci"),
    path('delete_data_applied', views.delete_data_applied, name="delete_data_applied"),
    #Health science model
    path('data_in_health_sci', views.data_in_health_sci, name="data_in_health_sci"),
    path('delete_data_health', views.delete_data_health, name="delete_data_health"),
    #Pure science model
    path('data_in_pure_sci', views.data_in_pure_sci, name="data_in_pure_sci"),
    path('delete_data_pure', views.delete_data_pure, name="delete_data_pure"),
    
    
]