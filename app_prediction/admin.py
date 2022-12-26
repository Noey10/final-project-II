from django.contrib import admin

from app_prediction.models import Prediction

# Register your models here.
class PredictionAdmin(admin.ModelAdmin):
    list_display = [
                    'highschool_grade', 
                    'professional_grade',
                    'compulsory_pro_grade',
                    'select_vocation_grade',
                    'compulsory_elective_1',
                    'compulsory_elective_2',
                    'foreign_language_grade',
                    'thai_grade',
                    'avg_grade',
                    'result_predict',
                    'predict_at',
                    ]
    search_fields = ['predict_at']
    list_filter = ['result_predict']


admin.site.register(Prediction, PredictionAdmin)