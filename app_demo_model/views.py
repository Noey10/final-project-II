from mimetypes import types_map
from django.shortcuts import render
import os
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import *
from .resources import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tablib import Dataset
import pandas as pd
import numpy as np

def condition(x):
    if x > 3.49:
        return 'excellent'
    elif x > 2.99:
        return 'very good'
    elif x > 2.49:
        return 'good'
    elif x > 1.99:
        return'medium'
    elif x > 1.49:
        return 'poor'
    else:
        return'very poor'

@login_required
def test_upload(request):
    if request.method == 'POST':
        # res = BioResource()
        branch = request.POST.get('major')
        if branch == '1' :
            res = DssiResource()
        elif branch == '2':
            res = IctResource()
        elif branch == '3':
            res = BioResource()
        elif branch == '4':
            res = ChemiResource()
        else: 
            print('error')
        
        dataset = Dataset()
        file = request.FILES['myfile']
       #check type file
        if file.name.endswith('csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('xlsx'):
            df = pd.read_excel(file)
        else :
            messages.info(request, "ต้องการไฟล์ของข้อมูลที่เป็น excel หรือ csv")
            return render(request, 'app_demo_model/test_upload_course.html')
        
        if df.dtypes['admission_grade'] == np.float64:
            df2 = pd.DataFrame()
            df2['major'] = df['major']
            df2['admission_grade'] = (df['admission_grade'].apply(condition))
            df2['gpa_year_1'] = df['gpa_year_1'].apply(condition)
            df2['thai'] = df['thai'].apply(condition)
            df2['math'] = df['math'].apply(condition)
            df2['sci'] = df['sci'].apply(condition)
            df2['society'] = df['society'].apply(condition)
            df2['hygiene'] = df['hygiene'].apply(condition)
            df2['art'] = df['art'].apply(condition)
            df2['career'] = df['career'].apply(condition)
            df2['langues'] = df['langues'].apply(condition)
            df2['status'] = df['status']
            df = df2
        
        import_data = dataset.load(df)
        result = res.import_data(dataset, dry_run=True, raise_errors=True)
        if not result.has_errors():
            res.import_data(dataset, dry_run=False)
        
        messages.success(request, "อัปโหลดข้อมูลสำเร็จ")
        print('upload success.')
    return render(request, 'app_demo_model/test_upload_course.html')

@login_required
def show_data_course(request):
    dssi = DSSI.objects.all()
    ict = ICT.objects.all()
    bio = BIO.objects.all()
    chemi = CHEMI.objects.all()
    
    total = dssi.count()+ict.count()+bio.count()+chemi.count()
    
    context = {
        'total': total,
        'dssi': dssi,
        'ict': ict,
        'bio': bio,
        'chemi': chemi,
    }
    return render(request, 'app_demo_model/show_data_course.html', context)
    
@login_required
def add_major(request):
    if request.method == 'POST':
        form = MajorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_major = Major()
            new_major.name = data['name']
            new_major.abbreviation = data['abbreviation']
            new_major.save()
    else:
        form = MajorForm()
        
    context = {
        'form': form,
    }
    return render(request, 'app_demo_model/add_major.html', context )
    
    





