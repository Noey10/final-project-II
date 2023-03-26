from django import forms
from .models import UserForecasts

class UserPredictForm(forms.ModelForm):
    
    class Meta:
        model = UserForecasts
        fields = ("student_id","branch", "admission_grade", "gpa_year_1", "thai", "math", "sci", "society", "hygiene", "art", "career", "language")
        labels = {
            "student_id": "รหัสนักศึกษา",
            "branch": "สาขาวิชา",
            "admission_grade": "เกรดเฉลี่ยรับเข้า",
            "gpa_year_1": "เกรดเฉลี่ยชั้นปีที่ 1",
            "thai": "เกรดวิชาภาษาไทย",
            "math": "เกรดวิชาคณิตศาสตร์",
            "sci": "เกรดวิชาวิทยาศาสตร์",
            "society": "เกรดวิชาสังคมศึกษา",
            "hygiene": "เกรดวิชาสุขศึกษาและพลศึกษา",
            "art": "เกรดวิชาศิลปศึกษา",
            "career": "เกรดวิชาการงานอาชีพ",
            "language": "เกรดวิชาภาษาต่างประเทศ",
        }
        widgets = {
            "student_id": forms.widgets.TextInput(attrs={'class':'form-control', 'placeholder': 'กรุณากรอกรหัสนักศึกษา'}),
            "branch": forms.Select(attrs={'class': 'form-select',}),
            "admission_grade": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4.00', 'min': '0', 'class': 'form-control', 'placeholder': '0.00 - 4.00',}),
            "gpa_year_1": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4.00', 'min': '0', 'class': 'form-control', 'placeholder': '0.00 - 4.00',}),
            "thai": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4.00', 'min': '0', 'class': 'form-control', 'placeholder': '0.00 - 4.00',}),
            "math": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4.00', 'min': '0', 'class': 'form-control', 'placeholder': '0.00 - 4.00',}),
            "sci": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4.00', 'min': '0', 'class': 'form-control', 'placeholder': '0.00 - 4.00',}),
            "society": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4.00', 'min': '0', 'class': 'form-control', 'placeholder': '0.00 - 4.00',}),
            "hygiene": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4.00', 'min': '0', 'class': 'form-control', 'placeholder': '0.00 - 4.00',}),
            "art": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4.00', 'min': '0', 'class': 'form-control', 'placeholder': '0.00 - 4.00',}),
            "career": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4.00', 'min': '0', 'class': 'form-control', 'placeholder': '0.00 - 4.00',}),
            "language": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4.00', 'min': '0', 'class': 'form-control', 'placeholder': '0.00 - 4.00',}),   
        }
        
        
class InputFilePredictForm(forms.Form):
    class Meta:
        model = UserForecasts
        fields = ("branch", "admission_grade", "gpa_year_1", "thai", "math", "sci", "society", "hygiene", "art", "career", "language", "status")