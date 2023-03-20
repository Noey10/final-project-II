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
def upload(request):
    user = request.user
    form = BranchForm()
    b = Branch.objects.all()
    if request.method == 'POST':
        res = DataResource()
        
        if user.is_teacher == True:
            user_branch = user.branch_id
            branch_fil = Branch.objects.filter(id=user_branch).values('id')
            for i in branch_fil:
                branch = i['id']
            # print('branch :', branch)
        else:
            branch = request.POST.get('branch')
            
        if branch == None:
            messages.info(request, "กรุณาเลือกสาขาวิชาที่ท่านต้องการอัปโหลดข้อมูล")
            return HttpResponseRedirect(reverse('upload'))
        else:
            dataset = Dataset()
            file = request.FILES['myfile']
            #check type file
            if file.name.endswith('csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('xlsx'):
                df = pd.read_excel(file)
            else :
                messages.info(request, "กรุณาอ่านข้อกำหนดการอัปโหลดไฟล์ข้อมูล และตรวจสอบข้อมูลของท่านอีกครั้ง")
                return HttpResponseRedirect(reverse('upload'))
            
        #ถ้ามีคอลัมน์ branch ให้ลบออกไปก่อน
        if 'branch' in df.columns.to_list():
            df = df.drop(['branch'], axis=1)
        else:
            print("ok")
            
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
            return HttpResponseRedirect(reverse('upload'))
            
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
    context = {
        'b': b,
        'form': form,
    }
    return render(request, 'app_demo_model/upload_data_model.html', context)

@login_required
@user_passes_test(check_user, login_url='error_page')
def show(request):
    user = request.user
    branch = Branch.objects.all()
    data = Data.objects.all()
    total = data.count()
    
    if user.is_teacher == True:
        print('teacher')
        user = user.branch_id
        print(user)
        branch = Branch.objects.get(id=user)
        print(branch)
        data = Data.objects.filter(branch_id=branch)
        total = data.count()
    
    context = {
        'branch': branch,
        'data': data,
        'total': total,
    }
    return render(request, 'app_demo_model/show_data.html', context)

@login_required
@user_passes_test(check_user, login_url='error_page')
def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()

        form = BranchForm()
        messages.success(request, "เพิ่มข้อมูลสาขาสำเร็จ")
        # return HttpResponseRedirect(reverse('upload'))
        return HttpResponseRedirect(request.headers.get("referer"))

@login_required
@user_passes_test(check_user, login_url='error_page')
def show_branch(request):
    branch = Branch.objects.all()
    context = {
        'branch': branch,
    }
    return render(request, 'app_demo_model/show_data_branch.html', context)

@login_required
@user_passes_test(check_user, login_url='error_page')
def delete_branch(request, id):
    branch = Branch.objects.filter(id=id)
    branch.delete()
    return HttpResponseRedirect(reverse('show_branch'))
    # return render(request, 'app_demo_model/show_data_branch.html')

@login_required
@user_passes_test(check_user, login_url='error_page')
def update_branch(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        abbreviation = request.POST['abbreviation']
        
        branch = Branch.objects.get(id=id)
        
        branch.name = name
        branch.abbreviation = abbreviation
        branch.save()
    messages.success(request, "อัปเดตข้อมูลสาขาสำเร็จ")
    return HttpResponseRedirect(reverse('show_branch'))

    