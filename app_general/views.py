from django.urls import reverse
from django.shortcuts import render
from app_prediction.models import UserPredict
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import pandas as pd
import numpy as np
from django.core.paginator import Paginator
from app_demo_model.models import *
from app_demo_model.resources import *
from django.contrib import messages
from tablib import Dataset

# Create your views here.
def check_user(user):
    return user.is_staff

@login_required
@user_passes_test(check_user, login_url='error_page')
def dashboard(request):
    data = UserPredict
    item = data.objects.all()
    total = item.count()
    print('total = ', total)  
        
    all_pass = data.objects.filter(status='Pass').count()
    all_fail = data.objects.filter(status='Fail').count()
    print('pass:', all_pass, ', ', 'fail:', all_fail)
    
    branch = Branch.objects.all()
    status_pass = []
    status_fail =[]
    for i in branch:
        b_status_p =  data.objects.filter(branch=i, status='Pass').count()
        status_pass.append(b_status_p)
        
        b_status_f =  data.objects.filter(branch=i, status='Fail').count()
        status_fail.append(b_status_f)
    
    per_pass = 0
    per_fail = 0
    if not all_pass == 0 :
        per_pass = round((all_pass/total)*100, 2)
        per_fail = round((all_fail/total)*100, 2)
        
    context = {
        'item': item,
        'branch': branch, 
        'total': total,
        'all_pass': all_pass,
        'all_fail': all_fail,
        'per_pass': per_pass,
        'per_fail': per_fail,
        'status_pass': status_pass,
        'status_fail': status_fail,
    }
    
    return render(request, 'app_general/dashboard.html', context)


def error_page(request):  
    
    data = UserPredict.objects.all().values()
    dat = pd.DataFrame(data)
    print(dat.head())
    return render(request, 'app_general/errors_page.html')

    if request.method == 'POST':
        res = DataResource()       
        branch = request.POST.get('branch')
        
        dataset = Dataset()
        
        file = request.FILES['myfile']
       #check type file
        if file.name.endswith('csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('xlsx'):
            df = pd.read_excel(file)
        else :
            messages.info(request, "กรุณาอ่านข้อกำหนดการอัปโหลดไฟล์ข้อมูล และตรวจสอบข้อมูลของท่านอีกครั้ง")
            return render(request, 'app_general/errors_page.html')
        
        print(df)
        if 'branch' in df.columns.to_list():
            df = df.drop(['branch'], axis=1)
        else:
            pass
        print("########################################")
        print(df)
        
        #ลบแถวที่มี missing value
        df = df.dropna()
        data_branch = []

        for i in range(len(df)):
            data_branch.append(branch)
            
        df_branch = pd.DataFrame(data_branch, columns=['branch'])
        
        df = pd.concat([df_branch, df], axis=1)
 
        #เช็ค column
        col = df.columns
        col_list =  col.to_list()
        
        categories_feature = ['branch', 'admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'langues', 'status']
        if col_list != categories_feature:
            messages.info(request, "กรุณาอ่านข้อกำหนดการอัปโหลดไฟล์ข้อมูล และตรวจสอบข้อมูลของท่านอีกครั้ง")
            return render(request, 'app_general/errors_page.html')
        
        #เช็ค type ของ column ถ้าเป็น float ก็แปลงเป็นช่วงเกรด
        for i in categories_feature:
            # print(df.dtypes[i])
            if df.dtypes[i] == np.float64:
                df[i] = df[i].apply(condition)
        
        import_data = dataset.load(df)
        result = res.import_data(dataset, dry_run=True, raise_errors=True)
        if not result.has_errors():
            res.import_data(dataset, dry_run=False)
        
        messages.success(request, "อัปโหลดข้อมูลสำเร็จ")
        print('upload success.')
        
    return render(request, 'app_general/errors_page.html')