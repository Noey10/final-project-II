from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('test_predict', views.test_predict, name='test_predict'),
    # path('test', views.test, name="test"),
    path('data_in_model', views.data_in_model, name="data_in_model"),
    path('delete_datas', views.delete_datas, name="delete_datas"),
    path('testing_predict', views.testing_predict, name="testing_predict"),
    path('show_data_input', views.show_data_input, name="show_data_input"),
    
    
]