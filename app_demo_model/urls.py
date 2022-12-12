from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('test_predict', views.test_predict, name='test_predict'),
    path('test', views.test, name="test"),

]