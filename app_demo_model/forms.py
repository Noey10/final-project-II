from django import forms
from attr import fields
from .models import AppliedScience, HealthScience, PureScience


class AppliedForm(forms.Form):
    class Meta:
        model = AppliedScience
        fields = '__all__'
        
class HealthForm(forms.Form):
    class Meta:
        model = HealthScience
        fields = '__all__'
        
class PureForm(forms.Form):
    class Meta:
        model = PureScience
        fields = '__all__'
