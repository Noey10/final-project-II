from django.db import models

# Create your models here.
class Grades(models.Model):
    major = models.CharField(default='', blank=True, max_length=50, null=True)
    gpa = models.CharField(default='', blank=True, max_length=50, null=True)
    admission_grade = models.CharField(default='', blank=True, max_length=50, null=True)
    gpa_year_1 = models.CharField(default='', blank=True, max_length=50, null=True)
    thai = models.CharField(default='', blank=True, max_length=50, null=True)
    mathematics = models.CharField(default='', blank=True, max_length=50, null=True)
    science = models.CharField(default='', blank=True, max_length=50, null=True)
    society = models.CharField(default='', blank=True, max_length=50, null=True)
    hygiene = models.CharField(default='', blank=True, max_length=50, null=True)
    art = models.CharField(default='', blank=True, max_length=50, null=True)
    career = models.CharField(default='', blank=True, max_length=50, null=True)
    english = models.CharField(default='', blank=True, max_length=50, null=True)
    status = models.CharField(default='', blank=True, max_length=50, null=True)