from django import forms
#from .models import Prediction

class PredictionForm(forms.Form):
    grade_choices = [(1, 'A'), (2, 'B+'), (3, 'B'), (4, 'C+'), (5, 'C'), (6, 'D+'), (7, 'D'), (8, 'F')]
    CHOICES2 = [('sci-math', 'sci-math'), ('art-math', 'art-math'), ('etc.', 'etc.')]
    CHOICES = [('True','Pass'), ('False', 'Not pass')]
    gender_choices = [('M','Male'),('F','Female')]
    
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=gender_choices, required=True, label='gender')
    plan_highschool = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES2, required=True, label='แผนการศึกษาระดับมัธยม')  
    highschool_grade = forms.ChoiceField(widget=forms.RadioSelect, choices=grade_choices, required=True, label='ผลการเรียนเฉลี่ยระดับมัธยม')  
    professional_grade = forms.ChoiceField(widget=forms.RadioSelect, choices=grade_choices, required=True, label='ผลการเรียนกลุ่มพื้นฐานวิชาชีพ')  
    compulsory_pro_grade = forms.ChoiceField(widget=forms.RadioSelect, choices=grade_choices, required=True, label='ผลการเรียนกลุ่มวิชาชีพบังคับ')  
    select_vocation_grade = forms.ChoiceField(widget=forms.RadioSelect, choices=grade_choices, required=True, label='ผลการเรียนกลุ่มวิชาชีพเลือก')  
    compulsory_elective_1 = forms.ChoiceField(widget=forms.RadioSelect, choices=grade_choices, required=True, label='ผลการเรียนวิชาเลือกเสรีภาคเรียนที่ 1')  
    compulsory_elective_2 = forms.ChoiceField(widget=forms.RadioSelect, choices=grade_choices, required=True, label='ผลการเรียนวิชาเลือกเสรีภาคเรียนที่ 2')
    foreign_language_grade = forms.ChoiceField(widget=forms.RadioSelect, choices=grade_choices, required=True, label='ผลการเรียนกลุ่มภาษาต่างประเทศ')  
    thai_grade = forms.ChoiceField(widget=forms.RadioSelect, choices=grade_choices, required=True, label='ผลการเรียนกลุ่มภาษาไทย')  
    avg_grade = forms.ChoiceField(widget=forms.RadioSelect, choices=grade_choices, required=True, label='ผลการเรียนเฉลี่ยในชั้นปีที่ 1')
    result_predict = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True, label='เรียนผ่าน?')
    
