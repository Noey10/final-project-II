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
        if branch == 'DSSI' :
            res = DssiResource()
        elif branch == 'ICT':
            res = IctResource()
        elif branch == 'bio':
            res = BioResource()
        elif branch == 'chemi':
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
        
        #ลบแถวที่มี missing value
        df = df.dropna()
        
        #เช็ค column ว่าตรงกันไหม
        col = df.columns
        col_list =  col.to_list()
        
        categories_feature = ['major', 'admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'langues', 'status']
        if col_list != categories_feature:
            messages.info(request, "ต้องการคอลัมน์ major, admission_grade, gpa_year_1, thai, math, sci, society, hygiene, art, career, langues, status")
            return render(request, 'app_demo_model/test_upload_course.html')
        
        #เช็ค type ของ column ถ้าเป็น float ก็แปลงเป็นช่วงเกรด
        for i in categories_feature:
            # print(df.dtypes[i])
            if df.dtypes[i] == np.float64:
                df[i] = df[i].apply(condition)
        # print(df.head())
        
        import_data = dataset.load(df)
        result = res.import_data(dataset, dry_run=True, raise_errors=True)
        if not result.has_errors():
            res.import_data(dataset, dry_run=False)
        
        messages.success(request, "อัปโหลดข้อมูลสำเร็จ")
        print('upload success.')
    return render(request, 'app_demo_model/test_upload_course.html')

@login_required
def show_data_course(request):
    searched = ''
    pass_status = 0
    fail_status = 0
    total = 0
    dssi = ''
    ict = ''
    bio = ''
    chemi = ''
    
    if request.method =='POST':
        searched = request.POST.get('major')
        if searched == 'DSSI':
            searched = 'วิทยาการคอมพิวเตอร์/วิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์'
            dssi = DSSI.objects.all()
            pass_status = DSSI.objects.filter(status__contains='Pass').count()
            fail_status = DSSI.objects.filter(status__contains='Fail').count()
            total = dssi.count()
        elif searched == 'ICT':
            searched = 'เทคโนโลยีสารสนเทศ/เทคโนโลยีสารสนเทศและการสื่อสาร'
            ict = ICT.objects.all()
            total = ict.count()
            pass_status = ICT.objects.filter(status__contains='Pass').count()
            fail_status = ICT.objects.filter(status__contains='Fail').count()
        elif searched == 'bio':
            searched ='ชีววิทยา'
            bio = BIO.objects.all()
            total = bio.count()
            pass_status = BIO.objects.filter(status__contains='Pass').count()
            fail_status = BIO.objects.filter(status__contains='Fail').count()
        elif searched == 'chemi':
            searched = 'เคมี'
            chemi = CHEMI.objects.all()
            total = chemi.count()
            pass_status = CHEMI.objects.filter(status__contains='Pass').count()
            fail_status = CHEMI.objects.filter(status__contains='Fail').count()
        else: 
            print('error branch')
    else:
        dssi = DSSI.objects.all()
        ict = ICT.objects.all()
        bio = BIO.objects.all()
        chemi = CHEMI.objects.all()
        
        total = dssi.count()+ict.count()+bio.count()+chemi.count()
    print('search = ', searched)
    context = {
        'search': searched,
        'total': total,
        'dssi': dssi,
        'ict': ict,
        'bio': bio,
        'chemi': chemi,
        'pass_status': pass_status,
        'fail_status': fail_status,
    }
    return render(request, 'app_demo_model/show_data_course.html', context)
    
   





