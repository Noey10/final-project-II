from django.db import models

# Create your models here.
class AppliedScience(models.Model):
    major = models.CharField( max_length=100)
    admission_grade = models.CharField(max_length=5)
    gpa_year_1 = models.CharField(max_length=5, null=False)
    thai = models.CharField(max_length=5, null=False)
    math = models.CharField(max_length=5, null=False)
    sci = models.CharField(max_length=5, null=False)
    society = models.CharField(max_length=5, null=False)
    hygiene = models.CharField(max_length=5, null=False)
    art = models.CharField(max_length=5, null=False)
    career = models.CharField(max_length=5, null=False)
    langues = models.CharField(max_length=5, null=False)
    status = models.CharField(max_length=50, null=False)

class HealthScience(models.Model):
    major = models.CharField(max_length=100)
    admission_grade = models.CharField(max_length=5)
    gpa_year_1 = models.CharField(max_length=5)
    thai = models.CharField(max_length=5)
    math = models.CharField(max_length=5)
    sci = models.CharField(max_length=5)
    society = models.CharField(max_length=5)
    hygiene = models.CharField(max_length=5)
    art = models.CharField(max_length=5)
    career = models.CharField(max_length=5)
    langues = models.CharField(max_length=5)
    status = models.CharField(max_length=50)
    
class PureScience(models.Model):
    major = models.CharField(max_length=100)
    admission_grade = models.CharField(max_length=5)
    gpa_year_1 = models.CharField(max_length=5)
    thai = models.CharField(max_length=5)
    math = models.CharField(max_length=5)
    sci = models.CharField(max_length=5)
    society = models.CharField(max_length=5)
    hygiene = models.CharField(max_length=5)
    art = models.CharField(max_length=5)
    career = models.CharField(max_length=5)
    langues = models.CharField(max_length=5)
    status = models.CharField(max_length=50)
    
    