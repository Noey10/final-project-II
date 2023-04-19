from django.urls import path
from . import views

urlpatterns = [
    path('form', views.form, name='form'),
    path('process_predict', views.prediction, name='process_predict'),
    path('information', views.information, name='information'),
    # path('download_file', views.download_file, name='download_file'),
    # path('delete_data_user_input', views.delete_data_user_input, name='delete_data_user_input'),    
    path('predict_for_admin', views.predict_for_admin, name='predict_for_admin'),    
    path('predict_group_student', views.predict_group_student, name='predict_group_student'),
    path('process_predict_group', views.process_predict_group, name='process_predict_group'),  
      
    
    
]