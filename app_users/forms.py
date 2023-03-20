from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django import forms
from app_users.models import User

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")
        
class TeacherForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "is_teacher", "title", "branch", "first_name", "last_name", "password1", "password2")
        widgets = {
            "username": forms.widgets.TextInput(attrs={'class':'form-control'}),
            "email": forms.widgets.EmailInput(attrs={'class':'form-control'}),
            "branch": forms.widgets.Select(attrs={'class':'form-select'}),
            "title": forms.widgets.Select(attrs={'class': 'form-select'}),
            "first_name": forms.widgets.TextInput(attrs={'class':'form-control'}),
            "last_name": forms.widgets.TextInput(attrs={'class':'form-control'}),       
            "password": forms.widgets.PasswordInput(attrs={'class':'form-control'}),
            "password2": forms.widgets.PasswordInput(attrs={'class':'form-control'}),    
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

class UpdateTeacherForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "title", "first_name", "last_name", "branch")
        widgets = {
            "title": forms.widgets.Select(attrs={'class': 'form-select'}),
        }
