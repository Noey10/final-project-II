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
from sklearn.inspection import permutation_importance
from tablib import Dataset
from io import BytesIO
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
import time
from django.db.models import Q

# Create your views here.
def check_user(user):
    return user.is_superuser or user.is_teacher

def check_admin(user):
    return user.is_superuser

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
        
        #ทำนายผล
        result = model.predict(df_predict)
        result2 = result[0]
        
        #ทำนายค่าความน่าจะเป็น
        probability = model.predict_proba(df_predict)
        proba = np.around(probability * 100, 2)
        
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
    
    #ตรวจสอบคอลัมน์ที่มีความสำคัญต่อการทำนาย
    feature_importance = permutation_importance(model, X, y, random_state=0)
    my_list = []
    for i in feature_importance.importances_mean.argsort()[::-1]:
        case = X.columns[i]
        my_list.append(case)

    branch_filter = Branch.objects.get(id=branch)

    context = {
        'result': result2,
        'probability': proba,
        'mylist': my_list,
        'branch': branch_filter,
    }
    
    return render(request, 'app_prediction/prediction_result.html', context)

@login_required
@user_passes_test(check_user, login_url='error_page')
def information(request):
    user = request.user
    branch = user.branch
    item = UserForecasts.objects.all()
    
    if user.is_teacher == True:
        data = item.filter(branch__name=branch, user__is_teacher=True) | item.filter(branch__name=branch, user__is_superuser=True)
    else:
        data =  item.filter(user__is_superuser=True) | item.filter(user__is_teacher=True)
    
    total = data.count()
  
    
    context={
        'data': data,
        'total': total,
    } 
    return render(request, 'app_prediction/show_data_input.html', context)
  
@login_required
@user_passes_test(check_user, login_url='error_page')    
def predict_for_admin(request): 
    return render(request, 'app_prediction/predict_options.html')

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
    user = request.user
    
    if request.method == 'POST':
        if user.is_teacher == True:
            branch = user.branch
        else:
            branch_input = request.POST.get('branch')
            branch = Branch.objects.get(pk=branch_input)

        #อ่านข้อมูลในดาต้าเบสเพื่อสร้าง df สำหรับฝึกโมเดล
        try:
            data = TrainingData.objects.filter(branch_id=branch).values()
            if data.count() > 100:
                df_model = pd.DataFrame(data)
            else:
                messages.info(request, "สาขาที่ท่านเลือกยังไม่พร้อมให้บริการ")
                return HttpResponseRedirect(reverse('predict_group_student'))
        except:
            messages.info(request, "กรุณาตรวจสอบการเลือกสาขาที่จะทำนาย")
            return HttpResponseRedirect(reverse('predict_group_student'))
        
        #อ่านไฟล์ที่อินพุตมา
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
            messages.info(request, "ต้องการไฟล์ข้อมูลประเภท XLSX หรือ CSV เท่านั้น")
            return HttpResponseRedirect(reverse('predict_group_student'))
               
        #ถ้ามีคอลัมน์ branch ให้ลบออกไปก่อน
        try:
            df_input = df_input.drop(['branch'], axis=1)
        except:
            pass
        
        df_predict = pd.DataFrame(columns=df_input.columns.to_list())
        #จัดช่วงเกรด
        for i in df_predict.columns.to_list():
            try:
                df_predict[i] = df_input[i].apply(condition)
            except:
                df_predict[i] = df_input[i]
        
        try:
            df_predict = df_predict.drop(['student_id'])
        except:
            df_predict = df_predict
        
        #เลือกคอลัมน์ที่ต้องการ
        categories_feature = ['admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'language']
        col_list = df_predict.columns.to_list()
        
        
        #ลบคอลัมน์ที่ไม่ต้องการ
        for item in col_list:
            if item not in categories_feature:
                df_predict = df_predict.drop(item, axis=1)
            else:
                pass
                
        #ตรวจสอบคอลัมน์ที่แตกต่าง
        missing = list(set(categories_feature) - set(col_list))
        # print('col diff = ', missing)
        if len(missing) != 0:
            messages.info(request, f'ต้องการคอลัมน์ { missing } กรุณาตรวจสอบไฟล์ข้อมูลของท่าน')
            return HttpResponseRedirect(reverse('predict_group_student'))
        
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
        
        #ตรวจสอบคอลัมน์ที่มีความสำคัญต่อการทำนาย
        feature_importance = permutation_importance(model, X, y, random_state=0)
        my_list = []
        for i in feature_importance.importances_mean.argsort()[::-1]:
            # print(f"{X.columns[i]} : {feature_importance.importances_mean[i]:.5f}")
            if feature_importance.importances_mean[i] > 0.0001:
                case = X.columns[i]
                my_list.append(case)
        
        # print('my_list = ', my_list)
        
        #สร้าง DataFrame ให้ผลลัพธ์
        df_result = pd.DataFrame(result, columns=['status'])
        df_probability = pd.DataFrame(np.around(probability*100, 2), columns=['probability_fail', 'probability_pass'])
        
        #สร้าง DataFrame ให้ branch ที่รับมาจาก input เพื่อบันทึกลงดาต้าเบส
        df_branch = pd.DataFrame({'branch': [branch] * len(df_input)})
        df_user = pd.DataFrame({'user': [User.objects.get(pk=user.id)] * len(df_input)})
        df_save = pd.concat([df_branch, df_input, df_result, df_probability, df_user], axis=1)
        
        #send data to show in HTML
        df_show = df_save.drop(columns=['branch'])
        dict_show = df_show.to_dict('records')#convert data frame to dictionary
        total = total_fail = len(df_save)
        
        #ลบข้อมูลการทำนายที่มีในฐานข้อมูล
        information = UserForecasts.objects.filter(branch=branch)
        information.delete()
        print('delete success.')
        
        #บันทึกข้อมูล
        for _, row in df_save.iterrows():
            try:
                item = UserForecasts(
                    branch = row['branch'],
                    student_id = row['student_id'],
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
                    status = row['status'],
                    probability_fail = row['probability_fail'],
                    probability_pass = row['probability_pass'],
                    user= row['user'],
                )
                item.save()
            except:
                item = UserForecasts(
                    branch = row['branch'],
                    # student_id = row['student_id'],
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
                    status = row['status'],
                    probability_fail = row['probability_fail'],
                    probability_pass = row['probability_pass'],
                    user= row['user'],
                )
                item.save()                

        print('save success.')
        
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
        'branch': branch,
        'mylist': my_list,
        }
    return render(request, 'app_prediction/group_result.html', context)


  