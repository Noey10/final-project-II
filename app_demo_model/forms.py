from django import forms
from attr import fields
from .models import *

class MajorForm(forms.ModelForm):
    class Meta:
        model = Major
        fields = ('name', 'abbreviation')
        labels = {
            "name": "ชื่อสาขา",
            "abbreviation": "ตัวย่อ",
        }
        
class DssiForm(forms.Form):
    class Meta:
        model = DSSI
        fields = '__all__'
    
class IctForm(forms.Form):
    class Meta:
        model = ICT
        fields = '__all__'
    
class BioForm(forms.Form):
    class Meta:
        model = BIO
        fields = '__all__'
    
class ChemiForm(forms.Form):
    class Meta:
        model = CHEMI
        fields = '__all__'
        