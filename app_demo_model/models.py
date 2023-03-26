from django.db import models

# Create your models here.
class Branch(models.Model):
    name = models.CharField(unique=True, default='', max_length=100)
    abbreviation = models.CharField(unique=True, default='', max_length=100)
    
    def __str__(self):
        return self.name
    
class TrainingData(models.Model):
    branch = models.ForeignKey('Branch', blank="True", null="True", on_delete=models.CASCADE)
    admission_grade = models.CharField(max_length=20)
    gpa_year_1 = models.CharField(max_length=20)
    thai = models.CharField(max_length=20)
    math = models.CharField(max_length=20)
    sci = models.CharField(max_length=20)
    society = models.CharField(max_length=20)
    hygiene = models.CharField(max_length=20)
    art = models.CharField(max_length=20)
    career = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.status