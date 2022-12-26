from django.db import models

# Create your models here.
class Prediction(models.Model):
    highschool_grade = models.CharField(max_length=50)
    professional_grade = models.CharField(max_length=50)
    compulsory_pro_grade = models.CharField(max_length=50)
    select_vocation_grade = models.CharField(max_length=50)
    compulsory_elective_1 = models.CharField(max_length=50)
    compulsory_elective_2 = models.CharField(max_length=50)
    foreign_language_grade = models.CharField(max_length=50)
    thai_grade = models.CharField(max_length=50)
    avg_grade = models.CharField(max_length=50)
    result_predict = models.CharField(max_length=50)
    predict_at = models.DateField(auto_now_add=True)
    