from django.db import models
from app_users.models import *
from app_demo_model.models import *

# Create your models here.
class UserPredict(models.Model):
    student_id = models.CharField(max_length=50, null=True)
    branch = models.ForeignKey('app_demo_model.Branch', on_delete=models.CASCADE)
    admission_grade = models.FloatField(max_length=10)
    gpa_year_1 = models.FloatField(max_length=10)
    thai = models.FloatField(max_length=10)
    math = models.FloatField(max_length=10)
    sci = models.FloatField(max_length=10)
    society = models.FloatField(max_length=10)
    hygiene = models.FloatField(max_length=10)
    art = models.FloatField(max_length=10)
    career = models.FloatField(max_length=10)
    langues = models.FloatField(max_length=10)
    status = models.CharField(max_length=10)
    predict_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('app_users.CustomUser', default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.status