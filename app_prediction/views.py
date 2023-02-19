import http
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserPredict
from .forms import UserPredictForm
from app_demo_model.models import *
from app_users.models import CustomUser
from django.contrib import messages
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import sklearn.metrics as metrics
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_validate
from tablib import Dataset
from io import BytesIO
from .resources import InputFilePredictResource
from django.db.models import Q
#######################################################

# Create your views here.
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
        major = request.POST.get('major')
        # print(major)
        
        #user input
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
        
        #เก็บเกรดที่ input เข้ามาลงใน list
        grade_list = [
            admission_grade,
            gpa_year_1,
            thai,
            math,
            sci,
            society,
            hygiene,
            art,
            career,
            langues,
        ]
        # print(grade_list)
        
        #แปลงเกรดจากทศนิยมเป็นตัวอักษร
        new_grades = []
        for i in grade_list:
            if float(i) > 3.50:
                i = 'excellent'
            elif float(i) > 2.99:
                i = 'very good'
            elif float(i) > 2.49:
                i = 'good'
            elif float(i) > 1.99:
                i = 'medium'
            elif float(i) > 1.49:
                i = 'poor'
            elif float(i) < 1.50:
                i = 'very poor'
            new_grades.append(i)
        # print(new_grades)
        
        #create data frame for data user input 
        my_dict = {
            'major': major,
            'admission_grade': new_grades[0],
            'gpa_year_1': new_grades[1],
            'thai': new_grades[2],
            'math': new_grades[3],
            'sci': new_grades[4],
            'society': new_grades[5],
            'hygiene': new_grades[6],
            'art': new_grades[7],
            'career': new_grades[8],
            'langues': new_grades[9]
        }
        df_new = pd.DataFrame([my_dict])      
        
        if form.is_valid():
            user_input= form.save(commit=False)
            user_input.user = request.user
            result2 = ''
            acc2 = 0
            #โค้ดทำนาย
            df = pd.DataFrame()
            if major == 'DSSI':
                print("เรียกโมเดล DSSI มาใช้จ้า")
                dssi = DSSI.objects.all().values()
                if not dssi.count() == 0:
                    df = pd.DataFrame(dssi)#crate data frame             
                else:
                    messages.info(request, 'สาขาที่คุณเลือกยังไม่พร้อมให้บริการในขณะนี้')
                    form = UserPredictForm()
                    return HttpResponseRedirect(reverse('form'))
                    
            elif major == 'ICT':
                print("เรียกโมเดล ICT มาใช้จ้า")
                ict = ICT.objects.all().values()
                if not ict.count() == 0 :
                    df = pd.DataFrame(ict)           
                else:
                    messages.info(request, 'สาขาที่คุณเลือกยังไม่พร้อมให้บริการในขณะนี้')
                    form = UserPredictForm()
                    return HttpResponseRedirect(reverse('form'))
            
            elif major == 'chemi':
                print("เรียกโมเดล CHEMI มาใช้จ้า")
                chemi = CHEMI.objects.all().values()
                if not chemi.count() == 0:
                    df = pd.DataFrame(chemi)#crate data frame             
                else: 
                    messages.info(request, 'สาขาที่คุณเลือกยังไม่พร้อมให้บริการในขณะนี้')
                    form = UserPredictForm()
                    return HttpResponseRedirect(reverse('form'))
                
            elif major == 'bio':
                print("เรียกโมเดล BIO มาใช้จ้า")
                bio = BIO.objects.all().values()
                if not bio.count() == 0:
                    df = pd.DataFrame(bio)#crate data frame             
                else: 
                    messages.info(request, 'สาขาที่คุณเลือกยังไม่พร้อมให้บริการในขณะนี้')
                    form = UserPredictForm()
                    return HttpResponseRedirect(reverse('form'))
            
            # print(df.head())
            
            categories_feature = ['major', 'admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'langues']
            
            #แบ่งข้อมูล X,y
            X = df[categories_feature]
            y = df['status']
                    
            categories_transforms = Pipeline(steps=[
                ('OneHotEncoder', OneHotEncoder(handle_unknown='ignore'))
            ])
            #เตรียมข้อมูล เอา col ที่เป็น เป็นสตริงมาทำ One hot encoder
            preprocessor = ColumnTransformer(remainder='passthrough', 
                                             transformers=[(
                                                'catagories', categories_transforms, categories_feature 
                                            )]
            )
            #ทำ pipeline และทำ decision tree กำหนดความลึกเป็น 6
            pipe = Pipeline(steps=[
                ('prep', preprocessor),
                ('tree', RandomForestClassifier(n_estimators=100, max_depth=6))
            ])

            cv_data = cross_validate(pipe, X, y, cv=10)#ทำ cross validation 10 ครั้ง

            acc = cv_data['test_score'].mean()
            acc2 = round(acc*100, 2)
            print('accuracy model : ', cv_data['test_score'].mean())

            pipe.fit(X, y)#model
            result = pipe.predict(df_new)#predict
            result2 = result[0]
            print(result2)    
            
            
            user_input.status = result2
            user_input.save()
            print('save success')
            form = UserPredictForm()
        
        branch = ''
        if major == 'DSSI':
            branch = 'สาขาวิทยาการคอมพิวเตอร์หรือสาขาวิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์'
        elif major == 'ICT':
            branch = 'สาขาเทคโนโลยีสารสนเทศหรือสาขาเทคโนโลยีและการสื่อสาร'
        elif major == 'chemi':
            branch = 'สาขาเคมี'
        elif major == 'bio':
            branch = 'สาขาชีววิทยา'
        else:
            branch = 'ไม่มีสาขาที่ระบุ'
                
        grade_dict = {
            'สาขา': branch,
            'เกรดเฉลี่ยมัธยมตอนปลาย': grade_list[0],
            'เกรดเฉลี่ยชั้นปีที่ 1': grade_list[1],
            'ภาษาไทย': grade_list[2],
            'คณิตศาสตร์': grade_list[3],
            'วิทยาศาสตร์': grade_list[4],
            'สังคมศึกษา ศาสนาและวัฒนธรรม': grade_list[5],
            'สุขศึกษาและพลศึกษา': grade_list[6],
            'ศิลปศึกษา': grade_list[7],
            'การงานอาชีพ': grade_list[8],
            'ภาษาต่างประเทศ': grade_list[9],
        }

    context = {
        'result': result2, 
        'acc': acc2,
        'grade_dict': grade_dict,
    }
    return render(request, 'app_prediction/prediction_result.html', context)
    

@login_required
def information(request):
    user = request.user
    if user.is_staff == True and user.is_superuser == True:
        searched=""
        pass_status = 0
        fail_status = 0
        if request.method =='POST':
            searched = request.POST['search']
            data = UserPredict.objects.filter(student_id__contains=searched)
        else:
            data = UserPredict.objects.all()
        # print(data)
        total = data.count() 
        print('total = ', total)
        context={
            'search': searched,
            'data': data,
            'total': total,
        } 
        return render(request, 'app_prediction/show_data_input.html', context)
    else:
        return render(request, 'app_general/errors_page.html')

@login_required
def result(request):
    return render(request, 'app_prediction/prediction_result.html')

@login_required
def download_file(request):
    data = UserPredict.objects.all().values()
    df = pd.DataFrame(data)
    df = df.drop('predict_at', axis=1)
    df = df.drop('user_id', axis=1)
   
    
    with BytesIO() as b:
        with pd.ExcelWriter(b) as writer:
            # You can add multiple Dataframes to an excel file
            # Using the sheet_name attribute
            df.to_excel(writer, sheet_name="DATA 1", index=False)
    
        filename = "dataset.xlsx"
    
        # imported from django.http
        res = HttpResponse(
            b.getvalue(), # Gives the Byte string of the Byte Buffer object
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        res['Content-Disposition'] = f'attachment; filename={filename}'
        return res

@login_required    
def delete_data_user_input(request):
    user = request.user
    if user.is_staff == True and user.is_superuser == True:
        data_input = UserPredict.objects.all()
        data_input.delete()
        return render(request, 'app_prediction/show_data_input.html')
    else:
        return render(request, 'app_general/errors_page.html')
    
@login_required
def predict_for_admin(request):
    user = request.user
    if user.is_staff == True and user.is_superuser == True:         
        return render(request, 'app_prediction/predict_for_admin.html')
    else:
        return render(request, 'app_general/errors_page.html')

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
def predict_group_student(request):
    user = request.user
    if user.is_staff == True and user.is_superuser == True:
        return render(request, 'app_prediction/prediction_group_student.html')
    else:
        return render(request, 'app_general/errors_page.html')
    
@login_required
def process_predict_group(request):
    user = request.user
    if user.is_staff == True and user.is_superuser == True:
        
        if request.method == 'POST':
            major = request.POST.get('major')
            if major == 'DSSI':
                print("เรียกโมเดล DSSI มาใช้จ้า")
                data = DSSI.objects.all().values()#read data in Applied Science
                if not data.count() == 0:
                    df = pd.DataFrame(data)#crate data frame             
                else:
                    messages.info(request, 'สาขาที่คุณเลือกยังไม่พร้อมให้บริการในขณะนี้')
                    form = UserPredictForm()
                    return HttpResponseRedirect(reverse('predict_group_student'))
            elif major == 'ICT':
                print("เรียกโมเดล ICT มาใช้จ้า")
                data = ICT.objects.all().values()
                if not data.count() == 0:
                    df = pd.DataFrame(data)            
                else:
                    messages.info(request, 'สาขาที่คุณเลือกยังไม่พร้อมให้บริการในขณะนี้')
                    form = UserPredictForm()
                    return HttpResponseRedirect(reverse('predict_group_student'))
            elif major == 'bio':
                print("เรียกโมเดล bio มาใช้จ้า")
                data = CHEMI.objects.all().values()
                if not data.count() == 0:
                    df = pd.DataFrame(data)       
                else:
                    messages.info(request, 'สาขาที่คุณเลือกยังไม่พร้อมให้บริการในขณะนี้')
                    form = UserPredictForm()
                    return HttpResponseRedirect(reverse('predict_group_student'))
            elif major == 'chemi':
                print("เรียกโมเดล Chemi มาใช้จ้า")
                data = BIO.objects.all().values()
                if not data.count() == 0:
                    df = pd.DataFrame(data)        
                else:
                    messages.info(request, 'สาขาที่คุณเลือกยังไม่พร้อมให้บริการในขณะนี้')
                    form = UserPredictForm()
                    return HttpResponseRedirect(reverse('predict_group_student'))
            else:
                print('error')
                messages.info(request, 'โมเดลการทำนายมีปัญหา')
                form = UserPredictForm()
                return HttpResponseRedirect(reverse('predict_group_student'))
            
            file = request.FILES['myfile']
            if file.name.endswith('csv'):
                df_input = pd.read_csv(file)
            elif file.name.endswith('xlsx'):
                df_input = pd.read_excel(file)
            else :
                messages.info(request, "ต้องการไฟล์ของข้อมูลที่เป็น excel หรือ csv")
                return render(request, 'app_prediction/prediction_group_student.html')
            
            col = df_input.columns
            col_list =  col.to_list()
            
            categories_feature = ['major', 'admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'langues']
            feature = ['student_id', 'major', 'admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'langues']
            
            if col_list != categories_feature and col_list != feature:
                messages.info(request, "ต้องการคอลัมน์ student_id, major, admission_grade, gpa_year_1, thai, math, sci, society, hygiene, art, career, langues")
                return render(request, 'app_prediction/prediction_group_student.html')
            
            #จัดเกรดให้เป็นช่วง                  
            df2 = pd.DataFrame(columns=feature)
            if col_list == categories_feature:
                for i in categories_feature:
                    print('equal categories feature')
                    if df_input.dtypes[i] == np.float64:
                        df2[i] = df_input[i].apply(condition)
                    elif df_input.dtypes[i] == np.int64:
                        df2[i] = df_input[i]
                    elif df_input.dtypes[i] == np.object_:
                        df2[i] = df_input[i]
                    else:
                        print('error process')
            elif col_list == feature:
                print('equal feature')
                for i in feature:
                    if df_input.dtypes[i] == np.float64:
                        df2[i] = df_input[i].apply(condition)
                    elif df_input.dtypes[i] == np.int64:
                        df2[i] = df_input[i]
                    elif df_input.dtypes[i] == np.object_:
                        df2[i] = df_input[i]
                    else:
                        print('error process')
            else:
                print('process covert grade error')
                        
            #แบ่งข้อมูล X,y
            X = df[categories_feature]
            y = df['status']
                    
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
                ('tree', RandomForestClassifier(n_estimators=100, max_depth=6))
            ])
            cv_data = cross_validate(pipe, X, y.values.ravel(), cv=10)#ทำ cross validation 10 ครั้ง

            acc = cv_data['test_score'].mean()
            acc2 = round(acc*100, 2)
            print('accuracy model : ', cv_data['test_score'].mean())

            pipe.fit(X, y.values.ravel())#model
            result = pipe.predict(df2)#predict
            # print(result)
            df_result = pd.DataFrame(result, columns=['status'])
            
            new = pd.concat([df_input, df_result], axis=1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            
            dataset = Dataset()
            res = InputFilePredictResource()
            
            #บันทึกข้อมูลลงฐานข้อมูล
            import_data = dataset.load(new)
            result = res.import_data(dataset, dry_run=True, raise_errors=True)
            if not result.has_errors():
                res.import_data(dataset, dry_run=False)
            print('process success.')
            total = len(new)
            print(total)
            
            #filter ข้อมูลตามสถานะ
            filt_pass = new['status'].str.contains('Pass')
            filt_fail = new['status'].str.contains('Fail')
            total_pass = len(new[filt_pass])
            total_fail = len(new[filt_fail])
            
            #คำนวนเปอร์เซ็นต์
            per_pass = round((total_pass/total)*100, 2)
            per_fail = round((total_fail/total)*100, 2)
            
            if 'student_id' in new:
                slt_df = new[new['status'] == 'Fail'] 
                # print(slt_df)
                student = slt_df['student_id']
                student_list = student.values.tolist()
            else:
                student_list = ['ไม่สามารถระบบุได้ เนื่องจากคุณไม่ได้เพิ่มรหัสนักศึกษา']
            #ฟิลเตอร์ข้อมูลรหัสนักศึกษาที่มีสถานะเป็น Fail
                
                
            
            context = {
                'df': new,
                'total': total,
                'total_pass': total_pass,
                'total_fail': total_fail,
                'per_pass': per_pass,
                'per_fail': per_fail,
                'gg': student_list,
                
            }
            
    return render(request, 'app_prediction/group_result.html', context)
    






