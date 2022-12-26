from django.contrib import admin
from app_demo_model.models import Grades, GradesInput

# Register your models here.
class GradesAdmin(admin.ModelAdmin):
    list_display = [
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
        'status'
    ]
    search_fields = ['status']
    list_filter = ['status']
admin.site.register(Grades, GradesAdmin)
    
class GradesInputAdmin(admin.ModelAdmin):
    list_display = [
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
        'status'
    ]
    search_fields = ['status']
    list_filter = ['status']

admin.site.register(GradesInput, GradesInputAdmin)