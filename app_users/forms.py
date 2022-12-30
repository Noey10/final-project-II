from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django import forms
from django.contrib.auth.models import User
from app_users.models import Profile

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", )
        
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        
        
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
            "university" : forms.Textarea(attrs={"rows": 3}),
        }