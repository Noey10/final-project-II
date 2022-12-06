from attr import fields
from django import forms
from .models import Grades


class GradesForm(forms.Form):
    class Meta:
        model = Grades
        fields = ['__all__']