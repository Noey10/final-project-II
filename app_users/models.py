from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
CHOICES = [
    ('นาย', 'นาย'),
    ('นางสาว', 'นางสาว'),
    ('นาง', 'นาง'),
    ('อาจารย์', 'อาจารย์'),
    ('ผศ.', 'ผู้ช่วยศาสตราจารย์'),
    ('รศ.', 'รองศาสตราจารย์'),
    ('ศ.', 'ศาสตราจารย์'),
]
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="อีเมล")
    is_teacher = models.BooleanField(default=False, blank=True, null=True, verbose_name="อาจารย์")
    title = models.CharField(choices=CHOICES, max_length=50, blank=True, null=True, verbose_name="คำนำหน้าชื่อ")
    branch = models.ForeignKey('app_demo_model.Branch', on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="สาขาวิชา")
    

# class Profile(models.Model):
#     gender = models.CharField(max_length=15, default="")
#     university = models.TextField(default="")
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
    
