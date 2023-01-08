from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django import forms
from app_users.models import CustomUser, Profile

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email", )
        
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email")
        labels = {
            "email": "อีเมล"
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "last_name" : forms.TextInput(attrs={"class": "form-control mt-2"}),
            "email" : forms.TextInput(attrs={"class": "form-control mt-2"}),
            
        }
        
        
        
class ExtendedProfileForm(forms.ModelForm):
    prefix = "extended"
    # name = 
    class Meta:
        model = Profile
        fields = ("gender", "university")
        labels = {
            "gender": "เพศ",
            "university": "มหาวิทยาลัย"
        }
        widgets = {
            "gender": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "university" : forms.Textarea(attrs={"class": "form-control mt-2", "style": "height: 120px;"}),
        }