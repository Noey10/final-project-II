from django.db import models

# Create your models here.
# class Subscription(models.Model):
#     STATUS = [
#         ('unapproved', 'Unapproved'),
#         ('approved', 'Approved'),
#         ('banned', 'Banned'),
#     ]
#     name = models.CharField(max_length=60)
#     email = models.EmailField(max_length=254, unique=True)
#     status = models.CharField(max_length=15, choices=STATUS, default='unapproved')
#     registered = models.DateTimeField(auto_now_add=True) 

# class Prediction(models.Model):
#     gender = models.CharField(max_length=30)
#     plan_highschool = models.CharField(max_length=50)
#     highschool_grade = models.CharField(max_length=50)
#     professional_grade = models.CharField(max_length=50)
#     compulsory_pro_grade = models.CharField(max_length=50)
#     select_vocation_grade = models.CharField(max_length=50)
#     compulsory_elective_1 = models.CharField(max_length=50)
#     compulsory_elective_2 = models.CharField(max_length=50)
#     foreign_language_grade = models.CharField(max_length=50)
#     thai_grade = models.CharField(max_length=50)
#     avg_grade = models.CharField(max_length=50)
#     result_predict = models.CharField(max_length=50)
#     predict_at = models.DateField(auto_now_add=True)
       
# class Member(models.Model):
#     name = models.CharField(max_length=60)
#     email = models.EmailField(max_length=254)
#     password = models.CharField(max_length=60)
#     univ = models.CharField(max_length=60)
#     gender = models.CharField(max_length=50)
#     result_predict = models.CharField(max_length=50)
#     predict_at = models.DateField(auto_now_add=True)
#     registered = models.DateTimeField(auto_now_add=True) 
    