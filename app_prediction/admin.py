from django.contrib import admin
from .models import UserPredict

# Register your models here.
class UserPredictAdmin(admin.ModelAdmin):
    list_display = [
        'major',
        'admission_grade',
        'gpa_year_1',
        'thai',
        'math',
        'sci',
        'society',
        'hygiene',
        'art',
        'career',
        'langues',
        'status',
        'predict_at',
        'user',
    ]
    search_fields = ['major']
    list_filter = ['status']

admin.site.register(UserPredict, UserPredictAdmin)