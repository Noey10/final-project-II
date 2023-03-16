from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django import forms
from app_users.models import User, Profile

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", )
        
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {
            "email": "อีเมล"
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "last_name" : forms.TextInput(attrs={"class": "form-control mt-2"}),
            "email" : forms.TextInput(attrs={"class": "form-control mt-2"}),
            
        }
        
        
CHOICES = [
    ('female', 'หญิง'),
    ('male', 'ชาย'),    
]
class ExtendedProfileForm(forms.ModelForm):
    prefix = "extended"
    class Meta:
        model = Profile
        fields = ("gender", "university")
        labels = {
            "gender": "เพศ",
            "university": "มหาวิทยาลัย"
        }
        widgets = {
            "gender": forms.RadioSelect(choices=CHOICES),
            "university" : forms.Textarea(attrs={"class": "form-control mt-2", "style": "height: 100px;"}),
        }

class TeacherForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "is_teacher", "branch", "first_name", "last_name", "password1", "password2")
        widgets = {
            "username": forms.widgets.TextInput(attrs={'class':'form-control'}),
            "email": forms.widgets.EmailInput(attrs={'class':'form-control'}),
            "branch": forms.widgets.Select(attrs={'class':'form-select'}),
            "first_name": forms.widgets.TextInput(attrs={'class':'form-control'}),
            "last_name": forms.widgets.TextInput(attrs={'class':'form-control'}),       
            "password": forms.widgets.PasswordInput(attrs={'class':'form-control'}),
            "password2": forms.widgets.PasswordInput(attrs={'class':'form-control'}),    
        }