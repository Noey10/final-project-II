from django import forms
from .models import UserPredict

class UserPredictForm(forms.ModelForm):
    
    class Meta:
        model = UserPredict
        fields = ("major", "admission_grade", "gpa_year_1", "thai", "math", "sci", "society", "hygiene", "art", "career", "langues")
        labels = {
            "major": "สาขา",
            "admission_grade": "เกรดเฉลี่ยรับเข้า",
            "gpa_year_1": "เกรดเฉลี่ยชั้นปีที่",
            "thai": "เกรดวิชาภาษาไทย",
            "math": "เกรดวิชาคณิตศาสตร์",
            "sci": "เกรดวิชาวิทยษศาสตร์",
            "society": "เกรดวิชาสังคมศึกษา",
            "hygiene": "เกรดวิชาสุขศึกษาและพลศึกษา",
            "art": "เกรดวิชาศิลปศึกษา",
            "career": "เกรดวิชาการงานอาชีพ",
            "langues": "เกรดวิชาภาษาต่างประเทศ",
        }
        widgets = {
            "major": forms.Select(attrs={'class': 'form-control',}),
            "admission_grade": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4', 'min': '0', 'class': 'form-control',}),
            "gpa_year_1": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4', 'min': '0', 'class': 'form-control',}),
            "thai": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4', 'min': '0', 'class': 'form-control',}),
            "math": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4', 'min': '0', 'class': 'form-control',}),
            "sci": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4', 'min': '0', 'class': 'form-control',}),
            "society": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4', 'min': '0', 'class': 'form-control',}),
            "hygiene": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4', 'min': '0', 'class': 'form-control',}),
            "art": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4', 'min': '0', 'class': 'form-control',}),
            "career": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4', 'min': '0', 'class': 'form-control',}),
            "langues": forms.widgets.NumberInput(attrs={'step': '0.01', 'max': '4', 'min': '0', 'class': 'form-control',}),   
        }