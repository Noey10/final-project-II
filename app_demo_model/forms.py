from attr import fields
from django import forms
from .models import Grades


class GradesForm(forms.Form):
    class Meta:
        model = Grades
        fields = ['gpa', 'admission_grade', 'gap_year_1', 'thai', 'mathematics', 'science', 'society', 'hygiene', 'art', 'career', 'english', 'status']