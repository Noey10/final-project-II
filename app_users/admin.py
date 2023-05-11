from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app_users.models import *

# Register your models here.
# admin.site.register(CustomUser, UserAdmin)
admin.site.register(User)