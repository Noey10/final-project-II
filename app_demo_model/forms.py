from attr import fields
from django import forms
from .models import Grades, GradesInput
      
#choices
# grade_choices = [
#     ('7', 'A'), 
#     ('6', 'B+'), 
#     ('5', 'B'), 
#     ('4', 'C+'), 
#     ('3', 'C'), 
#     ('2', 'D+'), 
#     ('1', 'D'), 
#     ('0', 'F')
#     ]        


grade_choices = [
    ('1', 'A'), 
    ('2', 'B+'), 
    ('3', 'B'), 
    ('4', 'C+'), 
    ('5', 'C'), 
    ('6', 'D+'), 
    ('7', 'D'), 
    ('8', 'F')
    ]        


choices = [
    ('A','A'),
    ('B+','B+'),
    ('B','B'),
    ('C+','C+'),
    ('C','C'),
    ('D+','D+'),
    ('D','D'),
    ('F','F'),
    ]   
class TestPredictionGradeForm(forms.ModelForm):
    class Meta: 
        model = GradesInput
        fields = [
            'gpa',
            'admission_grade',
            'gpa_year_1',
            'thai',
            'mathematics',
            'science',
            'society',
            'hygiene',
            'art',
            'career',
            'english',
        ]
        
        labels = {
            'gpa': 'GPA',
            'admission_grade': 'Admission grade',
            'gpa_year_1': 'GPA year 1',
            'thai': 'Thai',
            'mathematics': 'Math',
            'science': 'Sci',
            'society': 'Society',
            'hygiene': 'Hygiene',
            'art': 'Art',
            'career': 'Career',
            'english': 'English',
        }
    
        widgets = {
            'gpa': forms.RadioSelect(choices=grade_choices),
            'admission_grade': forms.RadioSelect(choices=grade_choices),
            'gpa_year_1': forms.RadioSelect(choices=grade_choices),
            'thai': forms.RadioSelect(choices=grade_choices),
            'mathematics': forms.RadioSelect(choices=grade_choices),
            'science': forms.RadioSelect(choices=grade_choices),
            'society': forms.RadioSelect(choices=grade_choices),
            'hygiene': forms.RadioSelect(choices=grade_choices),
            'art': forms.RadioSelect(choices=grade_choices),
            'career': forms.RadioSelect(choices=grade_choices),
            'english': forms.RadioSelect(choices=grade_choices),
        }