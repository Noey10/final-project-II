from django import forms
from attr import fields
from .models import *

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'
        
        
class DataForm(forms.Form):
    class Meta:
        model = TrainingData
        fields = '__all__'