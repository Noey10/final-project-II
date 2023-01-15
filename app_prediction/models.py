from django.db import models

# Create your models here.
class UserPredict(models.Model):
    major = models.CharField(max_length=50)
    admission_grade = models.CharField(max_length=10)
    gpa_year_1 = models.CharField(max_length=10)
    thai = models.CharField(max_length=10)
    math = models.CharField(max_length=10)
    sci = models.CharField(max_length=10)
    society = models.CharField(max_length=10)
    hygiene = models.CharField(max_length=10)
    art = models.CharField(max_length=10)
    career = models.CharField(max_length=10)
    langues = models.CharField(max_length=10)
    predict_at = models.DateTimeField(auto_now_add=True)
    
class UserResult(models.Model):
    status = models.CharField(max_length=45)
    # userpredictions = models.Fo(UserPredict)
    name = models.ForeignKey('UserPredict', on_delete=models.CASCADE)