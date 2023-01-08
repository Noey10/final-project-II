from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    gender = models.CharField(max_length=15, default="")
    # user_img = models.ImageField()
    university = models.TextField(default="")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)