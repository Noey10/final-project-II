from django import forms
from .models import Prediction

gender_choices = [
    ('M', 'Male'), ('F', 'Female')
]
grade_choices = [
    (1, 'A'), 
    (2, 'B+'), 
    (3, 'B'), 
    (4, 'C+'), 
    (5, 'C'), 
    (6, 'D+'), 
    (7, 'D'), 
    (8, 'F')
]
CHOICES2 = [
    ('sci-math', 'sci-math'),
    ('art-math', 'art-math'),
    ('etc.', 'etc.')
]
CHOICES = [
    ('True', 'Pass'), 
    ('False', 'Not pass')
]

class PredictionModelForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = [
                  'highschool_grade',
                  'professional_grade',
                  'compulsory_pro_grade',
                  'select_vocation_grade',
                  'compulsory_elective_1',
                  'compulsory_elective_2',
                  'foreign_language_grade',
                  'thai_grade',
                  'avg_grade',
                  ]
        
        labels = {
            'highschool_grade': 'ผลการเรียนเฉลี่ยระดับมัธยม',
            'professional_grade': 'ผลการเรียนกลุ่มพื้นฐานวิชาชีพ',
            'compulsory_pro_grade': 'ผลการเรียนกลุ่มวิชาชีพบังคับ',
            'select_vocation_grade': 'ผลการเรียนกลุ่มวิชาชีพเลือก',
            'compulsory_elective_1': 'ผลการเรียนวิชาเลือกเสรีภาคเรียนที่ 1',
            'compulsory_elective_2': 'ผลการเรียนวิชาเลือกเสรีภาคเรียนที่ 2',
            'foreign_language_grade': 'ผลการเรียนกลุ่มภาษาต่างประเทศ',
            'thai_grade': 'ผลการเรียนกลุ่มภาษาไทย',
            'avg_grade': 'ผลการเรียนเฉลี่ยในชั้นปีที่ 1',
        }
        
        widgets = {
            'highschool_grade': forms.RadioSelect(choices=grade_choices),
            'professional_grade': forms.RadioSelect(choices=grade_choices),
            'compulsory_pro_grade': forms.RadioSelect(choices=grade_choices),
            'select_vocation_grade': forms.RadioSelect(choices=grade_choices),
            'compulsory_elective_1': forms.RadioSelect(choices=grade_choices),
            'compulsory_elective_2': forms.RadioSelect(choices=grade_choices),
            'foreign_language_grade': forms.RadioSelect(choices=grade_choices),
            'thai_grade': forms.RadioSelect(choices=grade_choices),
            'avg_grade': forms.RadioSelect(choices=grade_choices),
        }