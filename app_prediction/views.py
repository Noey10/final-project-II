from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserPredict
from .forms import UserPredictForm
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

# Create your views here.
def check_user(user):
    return user.is_staff

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
def form(request):
    form = UserPredictForm()
    context={
        'form': form,
    } 
    return render(request, 'app_prediction/prediction_form.html', context)

@login_required
def prediction(request):
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
        langues = request.POST.get('langues')
        
        data = Data.objects.filter(branch__id__contains=branch).values()
        total_data = data.count()
        if total_data > 100:
            df_model = pd.DataFrame(data)
        else:
            messages.info(request, "ขออภัย สาขาที่ท่านเลือกยังไม่พร้อมให้บริการในขณะนี้")
            return HttpResponseRedirect(reverse('form')) 
        
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
            'langues': float(langues)
        }
        df_input = pd.DataFrame([my_dict])        
        
        categories_feature = ['admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'langues']
        df_predict = pd.DataFrame(columns=categories_feature)
        
        #จัดช่วงเกรด
        for i in categories_feature:
            if df_input.dtypes[i] == np.float64:
                df_predict[i] = df_input[i].apply(condition)
        
        if 'student_id' in df_predict.columns.to_list():
            df_predict = df_predict.drop(['student_id'], axis=1)
        elif 'branch' in df_predict.columns.to_list():
            df_predict = df_predict.drop(['branch'], axis=1)
        else:
            print('ok') 
            
        if form.is_valid():
            user_input = form.save(commit=False)
            user_input.user = request.user      
                        
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
            print('accuracy model : ', acc2, "%")
                        
            #model
            model = pipe.fit(X, y)
            #predict
            result = model.predict(df_predict)
            result2 = result[0]
            
            user_input.status = result2
            user_input.save()
            print('save success')
            form = UserPredictForm()
            
            grade_list = {
                'รหัสนักศึกษา': student_id,
                'สาขา': branch,
                'เกรดเฉลี่ยรับเข้า': admission_grade,
                'เกรดเฉลี่ยชั้นปี 1': gpa_year_1,
                'ภาษาไทย': thai,
                'คณิตศาสตร์': math,
                'วิทยาศาสตร์': sci,
                'สังคมศึกษา': society,
                'สุขศึกษาและพละศึกษา': hygiene,
                'ศิลปะ': art,
                'การงานอาชีพ': career,
                'ภาษาต่างประเทศ': langues 
            }
        else:
            form = UserPredictForm()
            
        context = {
            'grade_dict': grade_list,
            'result': result2,
        }
    
    return render(request, 'app_prediction/prediction_result.html', context)
    
@login_required
@user_passes_test(check_user, login_url='error_page')
def information(request):
    data = UserPredict.objects.all().order_by('-predict_at')
    total = data.count()
    
    searched=""
    if request.method =='POST':
        searched = request.POST['search']
        data = UserPredict.objects.filter(student_id__contains=searched).order_by('-predict_at')
        total = data.count()
    
    #Pagination
    page = Paginator(data, 11)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    
    print('total = ', total)
    context={
        'search': searched,
        'data': data,
        'total': total,
        'page': page,
    } 
    return render(request, 'app_prediction/show_data_input.html', context)

@login_required
@user_passes_test(check_user, login_url='error_page')
def download_file(request):
    data = UserPredict.objects.all().values()
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
    b = Branch.objects.all()
    context = {
        'b': b,
    }
    return render(request, 'app_prediction/prediction_group_student.html', context)
    
@login_required
def process_predict_group(request):
    if request.method == 'POST':
        branch = request.POST.get('branch')
        if branch != None:
            data = Data.objects.filter(branch__id__contains=branch).values()
            if data.count() > 100:
                df_model = pd.DataFrame(data)
            else:
                messages.info(request, "ขออภัย สาขาที่ท่านเลือกยังไม่พร้อมให้บริการในขณะนี้")
                return HttpResponseRedirect(reverse('predict_group_student'))   
        else:
            messages.info(request, "กรุณาตรวจสอบการเลือกสาขาที่จะทำนาย")
            return HttpResponseRedirect(reverse('predict_group_student'))
        
        #รับไฟล์
        file = request.FILES['myfile']
        if file.name.endswith('csv'):
            df_input = pd.read_csv(file)
        elif file.name.endswith('xlsx'):
            df_input = pd.read_excel(file)
        else :
            messages.info(request, "กรุณาอ่านข้อกำหนดการอัปโหลดไฟล์ข้อมูล และตรวจสอบข้อมูลของท่านอีกครั้ง")
            return HttpResponseRedirect(reverse('predict_group_student'))
        
        #ถ้ามีคอลัมน์ branch ให้ลบออกไปก่อน
        if 'branch' in df_input.columns.to_list():
            df_input = df_input.drop(['branch'], axis=1)
        else:
            print('ok')
                   
        #จัดช่วงเกรด
        df_predict = pd.DataFrame(columns=df_input.columns.to_list())
        for i in df_input.columns.to_list():
            if df_input.dtypes[i] == np.float64:
                df_predict[i] = df_input[i].apply(condition)
            elif df_input.dtypes[i] == np.int64:
                df_predict[i] = df_input[i].apply(condition)
            elif df_input.dtypes[i] == np.object_:
                df_predict[i] = df_input[i]
            else:
                print('error process')
            
        #ถ้ามีคอลัมน์ student_id ให้ลบออกไปก่อน
        if 'student_id' in df_predict.columns.to_list():
            df_predict = df_predict.drop(['student_id'], axis=1)
        else:
            print('ok') 
        
        categories_feature = ['admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'langues']        
        # เช็คคอลัมน์ว่าครบตามที่จะใช้ทำนายหรือไม่
        if df_predict.columns.to_list() != categories_feature:
            messages.info(request, "กรุณาอ่านข้อกำหนดการอัปโหลดไฟล์ข้อมูล และตรวจสอบข้อมูลของท่านอีกครั้ง")
            return HttpResponseRedirect(reverse('predict_group_student'))

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
        
        #ทำ pipeline steps
        pipe = Pipeline(steps=[
            ('prep', preprocessor),
            ('tree', RandomForestClassifier(n_estimators=100, max_depth=5))
        ])
        
        #ทำ cross validation 10 ครั้ง
        cv_data = cross_validate(pipe, X, y.values.ravel(), cv=10)
        
        #วัดประสิทธิภาพ
        acc = cv_data['test_score'].mean()
        acc2 = round(acc*100, 2)
        print('accuracy model : ', acc2)
        
        #model
        model = pipe.fit(X, y.values.ravel())
        
        #predict
        result = model.predict(df_predict)
        
        #สร้าง DataFrame ให้ผลลัพธ์
        df_result = pd.DataFrame(result, columns=['status'])
        
        #สร้าง DataFrame ให้ branch ที่รับมาจาก input เพื่อบันทึกลงดาต้าเบส
        data_branch = []
        for i in range(len(df_input)):
            data_branch.append(branch)
            
        df_branch = pd.DataFrame(data_branch, columns=['branch'])
        
        df_save = pd.concat([df_branch, df_input, df_result], axis=1)
        print(df_save.head())
        
        dataset = Dataset()
        res = InputFilePredictResource()
        
         #บันทึกข้อมูลลงฐานข้อมูล
        import_data = dataset.load(df_save)
        result = res.import_data(dataset, dry_run=True, raise_errors=True)
        if not result.has_errors():
            res.import_data(dataset, dry_run=False)
        print('process success.')
        total = len(df_save)
        print(total)
        
        #filter ข้อมูลตามสถานะ
        filt_pass = df_save['status'].str.contains('Pass')
        filt_fail = df_save['status'].str.contains('Fail')
        total_pass = len(df_save[filt_pass])
        total_fail = len(df_save[filt_fail])
        
        #คำนวนเปอร์เซ็นต์
        per_pass = round((total_pass/total)*100, 2)
        per_fail = round((total_fail/total)*100, 2)
        
        #ฟิลเตอร์ข้อมูลรหัสนักศึกษาที่มีสถานะเป็น Fail
        if 'student_id' in df_save:
            slt_df = df_save[df_save['status'] == 'Fail'] 
            student = slt_df['student_id']
            student_list = student.values.tolist()
        else:
            student_list = ['ไม่สามารถระบบุได้ เนื่องจากคุณไม่ได้เพิ่มรหัสนักศึกษา']
        
    context = {
            'df': df_save,
            'total': total,
            'total_pass': total_pass,
            'total_fail': total_fail,
            'per_pass': per_pass,
            'per_fail': per_fail,
            'gg': student_list,
            
        }
        
    return render(request, 'app_prediction/group_result.html', context)

@login_required
@user_passes_test(check_user, login_url='error_page')    
def delete_data_user_input(request):
    data_input = UserPredict.objects.all()
    data_input.delete()
    return render(request, 'app_prediction/show_data_input.html')
  




