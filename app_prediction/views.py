import http
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import UserPredict
from .forms import UserPredictForm
from app_demo_model.models import AppliedScience, HealthScience, PureScience
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import sklearn.metrics as metrics
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_validate

# Create your views here.
@login_required
def form(request):
    applied = AppliedScience.objects.all()
    health = HealthScience.objects.all()
    pure = PureScience.objects.all()
    form = UserPredictForm()
    context={
        'applied': applied,
        'health': health,
        'pure': pure,
        'form': form,
    } 
    return render(request, 'app_prediction/prediction_form.html', context)

@login_required
def prediction(request):
    if request.method == 'POST':
        form = UserPredictForm(request.POST)
        major = request.POST.get('major')
        print(major)
        
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
        
        #แปลงเกรดจากทศนิยมเป็นตัวอักษร
        new_grades = []
        for i in grade_list:
            if float(i) == 4.00:
                i = 'A'
            elif float(i) < 4.00 and float(i) > 3.49:
                i = 'B+'
            elif float(i) < 3.50 and float(i) > 2.99:
                i = 'B'
            elif float(i) < 3.00 and float(i) > 2.49:
                i = 'C+'
            elif float(i) < 2.50 and float(i) > 1.99:
                i = 'C'
            elif float(i) < 2.00 and float(i) > 1.49:
                i = 'D+'
            elif float(i) < 1.50 and float(i) > 0.99:
                i = 'D'
            elif float(i) < 1.00:
                i = 'F'
            new_grades.append(i)
        print(new_grades)
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
            
            #โค้ดทำนาย
            if major == 'DSSI' or major == 'ICT' or major == 'polymer':
                print("เรียกโมเดล Applied Science มาใช้จ้า")
                applied = AppliedScience.objects.all().values()#read data in Applied Science
                df = pd.DataFrame(applied)#crate data frame             
                #แบ่งข้อมูล X, y
                X = df.iloc[:, 1:-1]
                y = df.iloc[:, -1:]
                
                categories_feature = ['major', 'admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'langues']
                categories_transforms = Pipeline(steps=[
                    # ('Impure', SimpleImputer(strategy='constant', fill_value='missing')),
                    ('OneHotEncoder', OneHotEncoder(handle_unknown='ignore'))
                ])
                #เตรียมข้อมูล เอา col ที่เป็น เป็นสตริงมาทำ One hot encoder
                preprocessor = ColumnTransformer(remainder='passthrough',
                    transformers=[
                        ('catagories', categories_transforms, categories_feature )
                    ]
                )
                #ทำ pipeline และทำ decision tree กำหนดความลึกเป็น 6
                pipe = Pipeline(steps=[
                    ('prep', preprocessor),
                    ('tree', DecisionTreeClassifier(max_depth=6))
                ])
                # pipe = make_pipeline(prep2, DecisionTreeClassifier(max_depth=6))
                cv_data = cross_validate(pipe, X, y, cv=10)#ทำ cross validation 10 ครั้ง

                # print(cv_data['test_score'])#ดูเปอร์เซ็นต์ความถูกต้องของแต่ละรอบที่ทำ cross validation
                acc = cv_data['test_score'].mean()
                acc2 = round(acc*100, 2)
                print(cv_data['test_score'].mean())

                pipe.fit(X, y)#model
                result = pipe.predict(df_new)#predict
                result2 = result[0]
                print(result2)
                    
            elif major == 'safety'or major == 'enviSci':
                print("เรียกโมเดล Health Science มาใช้จ้า")
                health = HealthScience.objects.all().values()#read data in Applied Science
                df = pd.DataFrame(health)#crate data frame             
                X = df.iloc[:, 1:-1]
                y = df.iloc[:, -1:]
                
                categories_feature = ['major', 'admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'langues']
                categories_transforms = Pipeline(steps=[
                    # ('Impure', SimpleImputer(strategy='constant', fill_value='missing')),
                    ('OneHotEncoder', OneHotEncoder(handle_unknown='ignore'))
                ])
                #เตรียมข้อมูล เอา col ที่เป็น เป็นสตริงมาทำ One hot encoder
                preprocessor = ColumnTransformer(remainder='passthrough',
                    transformers=[
                        ('catagories', categories_transforms, categories_feature )
                    ]
                )
                #ทำ pipeline และทำ decision tree กำหนดความลึกเป็น 6
                pipe = Pipeline(steps=[
                    ('prep', preprocessor),
                    ('tree', DecisionTreeClassifier(max_depth=6))
                ])
                # pipe = make_pipeline(prep2, DecisionTreeClassifier(max_depth=6))
                cv_data = cross_validate(pipe, X, y, cv=10)#ทำ cross validation 10 ครั้ง

                # print(cv_data['test_score'])#ดูเปอร์เซ็นต์ความถูกต้องของแต่ละรอบที่ทำ cross validation
                acc = cv_data['test_score'].mean()
                acc2 = round(acc*100, 2)
                print(cv_data['test_score'].mean())

                pipe.fit(X, y)#model
                result = pipe.predict(df_new)#predict
                result2 = result[0]
                print(result2)
            
            elif major == 'math'or major == 'bio' or major == 'microBio' or major == 'physics' or major == 'chemi':
                print("เรียกโมเดล Pure Science มาใช้จ้า")
                pure = PureScience.objects.all().values()#read data in Applied Science
                df = pd.DataFrame(pure)#crate data frame             
                X = df.iloc[:, 1:-1]
                y = df.iloc[:, -1:]
                
                categories_feature = ['major', 'admission_grade', 'gpa_year_1', 'thai', 'math', 'sci', 'society', 'hygiene', 'art', 'career', 'langues']
                categories_transforms = Pipeline(steps=[
                    # ('Impure', SimpleImputer(strategy='constant', fill_value='missing')),
                    ('OneHotEncoder', OneHotEncoder(handle_unknown='ignore'))
                ])
                #เตรียมข้อมูล เอา col ที่เป็น เป็นสตริงมาทำ One hot encoder
                preprocessor = ColumnTransformer(remainder='passthrough',
                    transformers=[
                        ('catagories', categories_transforms, categories_feature )
                    ]
                )
                #ทำ pipeline และทำ decision tree กำหนดความลึกเป็น 6
                pipe = Pipeline(steps=[
                    ('prep', preprocessor),
                    ('tree', DecisionTreeClassifier(max_depth=6))
                ])
                # pipe = make_pipeline(prep2, DecisionTreeClassifier(max_depth=6))
                cv_data = cross_validate(pipe, X, y, cv=10)#ทำ cross validation 10 ครั้ง

                # print(cv_data['test_score'])#ดูเปอร์เซ็นต์ความถูกต้องของแต่ละรอบที่ทำ cross validation
                acc = cv_data['test_score'].mean()
                acc2 = round(acc*100, 2)
                print(cv_data['test_score'].mean())

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
        elif major == 'polymer':
            branch = 'สาขาเทคโนโลยีการยางและพอลิเมอร์'
        elif major == 'enviSci':
            branch = 'สาขาวิทยศาสตร์สิ่งแวดล้อม'
        elif major == 'safety':
            branch = 'สาขาอนามัยสิ่งแวดล้อมและความปลอดภัย'
        elif major == 'bio':
            branch = 'สาขาชีววิทยา'
        elif major == 'chemi':
            branch = 'สาขาเคมี'
        elif major == 'math':
            branch = 'สาขาคณิตศาสตร์'
        elif major == 'microBio':
            branch = 'สาขาจุลชีววิทยา'
        elif major == 'Physics':
            branch = 'สาขาฟิสิกส์หรือสาขาฟิสิกส์อุตสาหกรรมหรือสาขาฟิสิกส์ทางการแพทย์'
        else:
            branch = 'ไม่มีสาขาที่ระบุ'
                
        grade_dict = {
            'สาขาวิชา': branch,
            'เกรดเฉลี่ยมัธยมตอนปลาย': grade_list[0],
            'เกรดเฉลี่ยชั้นปีที่ 1': grade_list[1],
            'วิชาภาษาไทย': grade_list[2],
            'วิชาคณิตศาสตร์': grade_list[3],
            'วิชาวิทยาศาสตร์': grade_list[4],
            'วิชาสังคมศึกษา ศาสนาและวัฒนธรรม': grade_list[5],
            'วิชาสุขศึกษาและพลศึกษา': grade_list[6],
            'วิชาศิลปศึกษา': grade_list[7],
            'วิชาการงานอาชีพ': grade_list[8],
            'วิชาสุขศึกษาและพลศึกษา': grade_list[9]
        }

    context = {
        'result': result2, 
        'acc': acc2,
        'grade_dict': grade_dict
    }
    
    return render(request, 'app_prediction/prediction_result.html', context)
    

@login_required
def information(request):
    data = UserPredict.objects.all()
    total = data.count() 
    print('total = ', total)
    context={
      'data': data,
      'total': total,
    } 
    return render(request, 'app_prediction/show_data_input.html', context)

@login_required
def result(request):
    form = UserPredictForm()
    return render(request, 'app_prediction/prediction_result.html')