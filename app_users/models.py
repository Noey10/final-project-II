from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
CHOICES = [
    ('bio', 'ชีววิทยา'),
    ('chemi', 'เคมี'),
    ('DSSI', 'วิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์'),
    ('ICT', 'เทคโนโลยีสารสนเทศและการสื่อสาร'),
]
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="อีเมล")
    is_teacher = models.BooleanField(default=False, blank=True, null=True, verbose_name="อาจารย์")
    branch = models.CharField(default='bio', max_length=100, choices=CHOICES, blank=True, null=True, verbose_name="สาขาวิชา")
    

class Profile(models.Model):
    gender = models.CharField(max_length=15, default="")
    university = models.TextField(default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
