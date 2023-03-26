from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserForecasts
from .forms import UserPredictForm
from app_users.models import User
from app_demo_model.models import *
from django.contrib import messages
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate
from tablib import Dataset
from io import BytesIO
from .resources import InputFilePredictResource
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
import time

# Create your views here.
def check_user(user):
    return user.is_staff or user.is_teacher

@login_required
def form(request):
    form = UserPredictForm()
    context={
        'form': form,
    } 
    return render(request, 'app_prediction/prediction_form.html', context)

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
def prediction(request):
    t_start = time.time()
    result2 = ''
    proba = 0
    
    if request.method == 'POST':
        form = UserPredictForm(request.POST)

        #user input
        student_id = request.POST.get('student_id')
        branch = request.POST.get('branch')
        admission_grade = request.POST.get('admission_grade')
        gpa_year_1 = request.POST.get('gpa_year_1')
        thai = request.POST.get('thai')
        math = request.POST.get('math')
        sci = request.POST.get('sci')
        society = request.POST.get('society')
        hygiene = request.POST.get('hygiene')
        art = request.POST.get('art')
        career = request.POST.get('career')
        language = request.POST.get('language')
        
        data = TrainingData.objects.filter(branch__id__contains=branch).values()
        try:
            if data.count() < 100:
                messages.info(request, "สาขาที่ท่านเลือกยังไม่พร้อมให้บริการ")
                return HttpResponseRedirect(reverse('process_predict'))
            else:
                df_model = pd.DataFrame(data)
        except:
            messages.info(request, "สาขาที่ท่านเลือกยังไม่พร้อมให้บริการ")
            return HttpResponseRedirect(reverse('process_predict'))
        
        #create data frame for input data    
        my_dict = {
            'student_id': student_id,
            'branch': branch,
            'admission_grade': float(admission_grade),
            'gpa_year_1': float(gpa_year_1),
            'thai': float(thai),
            'math': float(math),
            'sci': float(sci),
            'society': float(society),
            'hygiene': float(hygiene),
            'art': float(art),
            'career': float(career),
            'language': float(language)
        }

        df_input = pd.DataFrame([my_dict])     
        # print('df input = ', df_input)
        
        categories_feature = ['admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'language']
        df_predict = pd.DataFrame(columns=categories_feature)
        #จัดช่วงเกรด
        for i in categories_feature:
            try:
                df_predict[i] = df_input[i].apply(condition)
            except:
                df_predict[i] = df_predict[i]
        
        # print('df predict = ', df_predict)
        
        try:
            df_predict = df_predict.drop(['student_id', 'branch'], axis=1)
        except:
            df_predict = df_predict

        # print('df predict = ', df_predict)
        
        #แบ่งข้อมูล X,y
        X = df_model[categories_feature]
        y = df_model['status']
        
        categories_transforms = Pipeline(steps=[
            ('OneHotEncoder', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        #เตรียมข้อมูล เอา col ที่เป็น เป็นสตริงมาทำ One hot encoder
        preprocessor = ColumnTransformer(remainder='passthrough', 
            transformers=[(
                'catagories', categories_transforms, categories_feature 
            )]
        )
        
        #ทำ pipeline และทำ decision tree กำหนดความลึกเป็น 5
        pipe = Pipeline(steps=[
            ('prep', preprocessor),
            ('tree', RandomForestClassifier(n_estimators=100, max_depth=5))
        ])
        
        #ทำ cross validation 10 ครั้ง
        cv_data = cross_validate(pipe, X, y, cv=10)
        
        #วัดประสิทธิภาพ
        acc = cv_data['test_score'].mean()
        acc2 = round(acc*100, 2)
        print('accuracy : ', acc2, "%")
        
        #model
        model = pipe.fit(X, y)
        
        
        #feature important
        # importance_df = pd.DataFrame({
        #     'feature': [categories_feature],
        #     'importance': model.feature_importances_
        # })
        # print('feature important', '\n', importance_df)
        
        #predict
        result = model.predict(df_predict)
        probability = model.predict_proba(df_predict)
        proba = np.around(probability * 100, 2)
        result2 = result[0]
        # print(proba)
        # print(result2)
                
        if form.is_valid():
            user_input = form.save(commit=False)
            user_input.user = request.user  
            user_input.status = result2
            user_input.probability_fail = proba[0, 0]
            user_input.probability_pass = proba[0, 1]
            user_input.save()
        else:
            form = UserPredictForm()

    t_end = time.time()
    print('time run : ', t_end-t_start)
    context = {
        # 'grade_dict': grade_list,
        'result': result2,
        'probability': proba,
        'acc': acc2,
    }
    
    return render(request, 'app_prediction/prediction_result.html', context)
    
@login_required
@user_passes_test(check_user, login_url='error_page')
def information(request):
    user = request.user
    user_admin = request.user.is_superuser
    user_teacher = request.user.is_teacher
    item = UserForecasts
    
    print('user = ', user)
    t_start = time.time()
    if user.is_superuser or user.is_staff == True:
        data = item.objects.filter(user_id=user_teacher) | item.objects.filter(user_id=user_admin)
        data = data.order_by('-predict_at')
        total = data.count()
        
    else:
        branch = request.user.branch_id
        print('branch = ', branch)
        id_branch = Branch.objects.get(id=branch)
        data = item.objects.filter(branch_id=id_branch, user_id=user_teacher) | item.objects.filter(branch_id=id_branch, user_id=user_admin)
        data = data.order_by('-predict_at')
        total = data.count()    
    
    print('total = ', total)
    t_end = time.time()
    print('time run = ', t_end-t_start)
    context={
        'data': data,
        'total': total,
    } 
    return render(request, 'app_prediction/show_data_input.html', context)

    
@login_required
@user_passes_test(check_user, login_url='error_page')
def download_file(request):
    user = request.user
    if user.is_teacher == True:
        user_branch = user.branch
        print(user_branch)
        branch = Branch.objects.get(abbreviation=user_branch)
        print(branch)
        data = UserForecasts.objects.filter(branch_id=branch).values()
        # print(data)
    
    else:
        data = UserForecasts.objects.all().values()
        # print(data)
        
    df = pd.DataFrame(data)
    df = df.drop('predict_at', axis=1)
    df = df.drop('user_id', axis=1)
   
    with BytesIO() as b:
        with pd.ExcelWriter(b) as writer:
            
            #ตั้งชื่อ sheet
            df.to_excel(writer, sheet_name="DATA 1", index=False)
            
        #ตั้งชื่อ file
        filename = "dataset.xlsx"
    
        res = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        res['Content-Disposition'] = f'attachment; filename={filename}'
        return res
  
@login_required
@user_passes_test(check_user, login_url='error_page')    
def predict_for_admin(request): 
    return render(request, 'app_prediction/predict_for_admin.html')

@login_required
@user_passes_test(check_user, login_url='error_page')   
def predict_group_student(request):
    user = request.user
    if user.is_teacher:
        user_branch = user.branch
        b = Branch.objects.filter(abbreviation=user_branch)
    else:
        b = Branch.objects.all()
    context = {
        'b': b,
    }
    return render(request, 'app_prediction/prediction_group_student.html', context)
    
@login_required
@user_passes_test(check_user, login_url='error_page')
def process_predict_group(request):
    t_start = time.time()
    user=request.user
    
    if request.method == 'POST':
        if user.is_superuser == True or user.is_staff == True:
            branch = request.POST.get('branch')
        else:
            user_branch = user.branch.id
            branch = Branch.objects.filter(id=user_branch).values('id')   
            for i in branch :
                branch =i['id']
            
        try:
            data = TrainingData.objects.filter(branch__id__contains=branch).values()
            if data.count() > 100:
                df_model = pd.DataFrame(data)
            else:
                messages.info(request, "สาขาที่ท่านเลือกยังไม่พร้อมให้บริการ")
                return HttpResponseRedirect(reverse('predict_group_student'))
        except:
            messages.info(request, "กรุณาตรวจสอบการเลือกสาขาที่จะทำนาย")
            return HttpResponseRedirect(reverse('predict_group_student'))
        
        #รับไฟล์
        file = request.FILES['myfile']
        try:
            if file.name.endswith('csv'):
                df_input = pd.read_csv(file)
                check_nan = df_input.isna().sum().sum()
                if check_nan != 0 :
                    # nan_rows  = df_input[df_input.isna().any(axis=1)]
                    messages.info(request, "ข้อมูลของท่านมีค่าว่างระบบไม่สามารถประวลผลได้ กรุณาตรวจสอบข้อมูลของท่านอีกครั้ง")
                    return HttpResponseRedirect(reverse('predict_group_student'))
            else:
                df_input = pd.read_excel(file)
                check_nan = df_input.isna().sum().sum()
                if check_nan != 0 :
                    # nan_rows  = df_input[df_input.isna().any(axis=1)]
                    messages.info(request, "ข้อมูลของท่านมีค่าว่างระบบไม่สามารถประวลผลได้ กรุณาตรวจสอบข้อมูลของท่านอีกครั้ง")
                    return HttpResponseRedirect(reverse('predict_group_student'))
        except:
            messages.info(request, "กรุณาอ่านข้อกำหนดการอัปโหลดไฟล์ข้อมูล และตรวจสอบข้อมูลของท่านอีกครั้ง")
            return HttpResponseRedirect(reverse('predict_group_student'))
        
        #ถ้ามีคอลัมน์ branch ให้ลบออกไปก่อน
        try:
            df_input = df_input.drop([ 'branch'], axis=1)
        except:
            df_input = df_input
        
        #จัดช่วงเกรด
        df_predict = pd.DataFrame(columns=df_input.columns.to_list())
        for i in df_input.columns.to_list():
            try:
                df_predict[i] = df_input[i].apply(condition)
            except:
                df_predict[i] = df_input[i]

        try: 
            df_predict = df_predict.drop(['student_id', 'branch'], axis=1)
        except:
            df_predict = df_predict

        categories_feature = ['admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'language']   
        # check_col = df_predict.columns.to_list()
        # print('check columns = ', check_col)
        # if check_col != categories_feature: 
        #     messages.info(request, "กรุณาอ่านข้อกำหนดการอัปโหลดไฟล์ข้อมูล และตรวจสอบข้อมูลของท่านอีกครั้ง")
        #     return HttpResponseRedirect(reverse('predict_group_student'))
        
        #Train model แบ่งข้อมูล X,y
        X = df_model[categories_feature]
        y = df_model['status']
        
        categories_transforms = Pipeline(steps=[
            ('OneHotEncoder', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        #เตรียมข้อมูล เอา col ที่เป็น เป็นสตริงมาทำ One hot encoder
        preprocessor = ColumnTransformer(remainder='passthrough', 
            transformers=[(
                'catagories', categories_transforms, categories_feature 
            )]
        )
        
        #ทำ pipeline steps
        pipe = Pipeline(steps=[
            ('prep', preprocessor),
            ('tree', RandomForestClassifier(n_estimators=100, max_depth=5))
        ])
        
        #ทำ cross validation 10 ครั้ง
        cv_data = cross_validate(pipe, X, y.values.ravel(), cv=10)
        
        #วัดประสิทธิภาพโมเดล
        acc = cv_data['test_score'].mean()
        acc2 = round(acc*100, 2)
        print('accuracy : ', acc2)
        
        #model
        model = pipe.fit(X, y)
        #predict
        result = model.predict(df_predict)
        
        #ทำนายความน่าจะเป็นของผลลัพธ์        
        probability = model.predict_proba(df_predict)
        
         #สร้าง DataFrame ให้ผลลัพธ์
        df_result = pd.DataFrame(result, columns=['status'])
        df_probability = pd.DataFrame(np.around(probability*100, 2), columns=['probability_fail', 'probability_pass'])
        
        #สร้าง DataFrame ให้ branch ที่รับมาจาก input เพื่อบันทึกลงดาต้าเบส
        df_branch = pd.DataFrame({'branch': [branch] * len(df_input)})
        df_save = pd.concat([df_branch, df_input, df_result, df_probability], axis=1)
        
        #send data to show in HTML
        df_show = df_save.drop(columns=['branch'])
        dict_show = df_show.to_dict('records')#convert data frame to dictionary
        total = total_fail = len(df_save)
        
        #ลบข้อมูลการทำนายที่มีในฐานข้อมูล
        information = UserForecasts.objects.filter(branch__id__contains=branch)
        information.delete()
        
        #บันทึกข้อมูลลงฐานข้อมูล
        # dataset = Dataset()
        # res = InputFilePredictResource()
        # import_data = dataset.load(df_save)
        # result = res.import_data(dataset, dry_run=True, raise_errors=True)
        # if not result.has_errors():
        #     res.import_data(dataset, dry_run=False)
                 
        #filter ข้อมูลตามสถานะ
        filt_pass = df_save['status'].str.contains('Pass')
        filt_fail = df_save['status'].str.contains('Fail')
        total_pass = len(df_save[filt_pass])
        total_fail = len(df_save[filt_fail])
        
    t_end = time.time()
    print('time run : ', t_end-t_start)
    context = {
        'df': dict_show,
        'total': total,
        'total_pass': total_pass,
        'total_fail': total_fail,
        'acc': acc2,
        }
    return render(request, 'app_prediction/group_result.html', context)

@login_required
@user_passes_test(check_user, login_url='error_page')    
def delete_data_user_input(request):
    data_input = UserForecasts.objects.all()
    data_input.delete()
    return render(request, 'app_prediction/show_data_input.html')
  