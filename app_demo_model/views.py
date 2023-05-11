from django.shortcuts import render
from django.http import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import *
from app_users.models import *
from .resources import *
from .forms import *
from django.contrib import messages
from tablib import Dataset
import pandas as pd
import numpy as np
from django.core.paginator import Paginator
import time

def check_user(user):
    return user.is_staff or user.is_teacher

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
@user_passes_test(check_user, login_url='error_page')
def upload_training_data(request):
    user = request.user
    form = BranchForm()
    b = Branch.objects.all()
    
    if request.method == 'POST':
        file = request.FILES['myfile']
        #check type file
        if file.name.endswith('csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('xlsx'):
             df = pd.read_excel(file)
        else: 
            messages.info(request, "ต้องการไฟล์ข้อมูลประเภท XLSX หรือ CSV เท่านั้น")
            return HttpResponseRedirect(reverse('upload'))
        
        
        if 'branch' in df.columns.to_list():
                df = df.drop(['branch'], axis=1)
        else:
            pass
        
        if user.is_teacher == True:
            branch = user.branch
        else:
            branch_input = request.POST.get('branch')
            branch = Branch.objects.get(pk=branch_input)
        
        data_branch = []
        for i in range(len(df)):
            data_branch.append(branch)
                
        df_branch = pd.DataFrame(data_branch, columns=['branch'])
           
        df = pd.concat([df_branch, df], axis=1)
        
        col_list = df.columns.tolist()       
        categories_feature = ['branch', 'admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'language', 'status']
        # print('len categories = ', len(categories_feature))
        
        #ลบคอลัมน์ที่ไม่ต้องการ
        for item in col_list:
            if item not in categories_feature:
                df = df.drop(item, axis=1)
                # print(f"{item} ไม่อยู่ใน categories_feature")
            else:
                pass
                # print(f"{item} อยู่ใน categories_feature")
        
        #ตรวจสอบคอลัมน์ที่แตกต่าง
        missing = list(set(categories_feature) - set(col_list))
        print('col diff = ', missing)
        if len(missing) != 0:
            messages.info(request, f'ต้องการคอลัมน์ { missing } กรุณาตรวจสอบไฟล์ข้อมูลของท่าน')
            return HttpResponseRedirect(reverse('upload'))
            
        #เช็ค type ของ column ถ้าเป็น float ก็แปลงเป็นช่วงเกรด
        for i in categories_feature:
            if df.dtypes[i] == np.float64:
                df[i] = df[i].apply(condition)
                # df[i] = df[i].apply(con)
        
        #บันทึกข้อมูล
        for _, row in df.iterrows():
            item = TrainingData(
                branch = row['branch'],
                admission_grade = row['admission_grade'],
                gpa_year_1 = row['gpa_year_1'],
                thai = row['thai'],
                math = row['math'],
                sci = row['sci'],
                society = row['society'],
                hygiene = row['hygiene'],
                art = row['art'],
                career = row['career'],
                language = row['language'],
                status = row['status']
            )
            item.save()
        
        messages.success(request, "อัปโหลดข้อมูลสำเร็จ")
        print('upload success.')
    
    context = {
        'b': b,
        'form': form,
    }
    return render(request, 'app_demo_model/upload_data_model.html', context)

@login_required
@user_passes_test(check_user, login_url='error_page')
def show_training_data(request):
    t_start = time.time()
    user = request.user
    branch = Branch.objects.all()
    data = TrainingData.objects.all()
    total = data.count()
    
    
    if user.is_teacher == True:
        print('teacher')
        user = user.branch_id
        print(user)
        branch = Branch.objects.get(id=user)
        print(branch)
        data = TrainingData.objects.filter(branch_id=branch)
        total = data.count()
        
    t_end = time.time()
    print('time run = ', t_end-t_start)
    context = {
        'branch': branch,
        'data': data,
        'total': total,
    }
    return render(request, 'app_demo_model/show_data.html', context)

@login_required
@user_passes_test(check_user, login_url='error_page')
def delete_data(request):
    data = TrainingData.objects.all()
    data.delete()
    return render(request, 'app_demo_model/show_data.html')

@login_required
@user_passes_test(check_user, login_url='error_page')
def show_branch(request):
    branch = Branch.objects.all()
    context = {
        'branch': branch,
    }
    return render(request, 'app_demo_model/show_data_branch.html', context)
