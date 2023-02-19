from django.db import models

# Create your models here.
#อันใหม่
class DSSI(models.Model):
    major = models.CharField(default='', max_length=100)
    admission_grade = models.CharField(max_length=20)
    gpa_year_1 = models.CharField(max_length=20)
    thai = models.CharField(max_length=20)
    math = models.CharField(max_length=20)
    sci = models.CharField(max_length=20)
    society = models.CharField(max_length=20)
    hygiene = models.CharField(max_length=20)
    art = models.CharField(max_length=20)
    career = models.CharField(max_length=20)
    langues = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.major
    
class ICT(models.Model):
    major = models.CharField(default='', max_length=100)
    admission_grade = models.CharField(max_length=20)
    gpa_year_1 = models.CharField(max_length=20)
    thai = models.CharField(max_length=20)
    math = models.CharField(max_length=20)
    sci = models.CharField(max_length=20)
    society = models.CharField(max_length=20)
    hygiene = models.CharField(max_length=20)
    art = models.CharField(max_length=20)
    career = models.CharField(max_length=20)
    langues = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.major

class BIO(models.Model):
    major = models.CharField(default='', max_length=100)
    admission_grade = models.CharField(max_length=20)
    gpa_year_1 = models.CharField(max_length=20)
    thai = models.CharField(max_length=20)
    math = models.CharField(max_length=20)
    sci = models.CharField(max_length=20)
    society = models.CharField(max_length=20)
    hygiene = models.CharField(max_length=20)
    art = models.CharField(max_length=20)
    career = models.CharField(max_length=20)
    langues = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.major

class CHEMI(models.Model):
    major = models.CharField(default='', max_length=100)
    admission_grade = models.CharField(max_length=20)
    gpa_year_1 = models.CharField(max_length=20)
    thai = models.CharField(max_length=20)
    math = models.CharField(max_length=20)
    sci = models.CharField(max_length=20)
    society = models.CharField(max_length=20)
    hygiene = models.CharField(max_length=20)
    art = models.CharField(max_length=20)
    career = models.CharField(max_length=20)
    langues = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.major

