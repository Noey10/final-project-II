from django.contrib import admin
from .models import *

# Register your models here.
# class ScienceModelAdmin(admin.ModelAdmin):
#     list_display = [
#         'branch',
#         'admission_grade',
#         'gpa_year_1',
#         'thai',
#         'math',
#         'sci',
#         'society',
#         'hygiene',
#         'art',
#         'career',
#         'language',
#         'status',
#     ]
#     search_fields = ['branch']
#     list_filter = ['status']
admin.site.register(TrainingData)
admin.site.register(Branch)
