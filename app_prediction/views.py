from django.shortcuts import render
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import UserPredict, UserAnswer
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
        if float(admission_grade) == 4.00:
            admission_grade = 'A'
        elif float(admission_grade) < 4.00 and float(admission_grade) > 3.49:
            admission_grade = 'B+'
        elif float(admission_grade) < 3.50 and float(admission_grade) > 2.99:
            admission_grade = 'B'
        elif float(admission_grade) < 3.00 and float(admission_grade) > 2.49:
            admission_grade = 'C+'
        elif float(admission_grade) < 2.50 and float(admission_grade) > 1.99:
            admission_grade = 'C'
        elif float(admission_grade) < 2.00 and float(admission_grade) > 1.49:
            admission_grade = 'D+'
        elif float(admission_grade) < 1.50 and float(admission_grade) > 0.99:
            admission_grade = 'D'
        elif float(admission_grade) < 1.00:
            admission_grade = 'F'
        gpa_year_1 = request.POST.get('gpa_year_1')
        if float(gpa_year_1) == 4.00:
            gpa_year_1 = 'A'
        elif float(gpa_year_1) < 4.00 and float(gpa_year_1) > 3.49:
            gpa_year_1 = 'B+'
        elif float(gpa_year_1) < 3.50 and float(gpa_year_1) > 2.99:
            gpa_year_1 = 'B'
        elif float(gpa_year_1) < 3.00 and float(gpa_year_1) > 2.49:
            gpa_year_1 = 'C+'
        elif float(gpa_year_1) < 2.50 and float(gpa_year_1) > 1.99:
            gpa_year_1 = 'C'
        elif float(gpa_year_1) < 2.00 and float(gpa_year_1) > 1.49:
            gpa_year_1 = 'D+'
        elif float(gpa_year_1) < 1.50 and float(gpa_year_1) > 0.99:
            gpa_year_1 = 'D'
        elif float(gpa_year_1) < 1.00:
            gpa_year_1 = 'F'
        thai = request.POST.get('thai')
        if float(thai) == 4.00:
            thai = 'A'
        elif float(thai) < 4.00 and float(thai) > 3.49:
            thai = 'B+'
        elif float(thai) < 3.50 and float(thai) > 2.99:
            thai = 'B'
        elif float(thai) < 3.00 and float(thai) > 2.49:
            thai = 'C+'
        elif float(thai) < 2.50 and float(thai) > 1.99:
            thai = 'C'
        elif float(thai) < 2.00 and float(thai) > 1.49:
            thai = 'D+'
        elif float(thai) < 1.50 and float(thai) > 0.99:
            thai = 'D'
        elif float(thai) < 1.00:
            thai = 'F'
        math = request.POST.get('math')
        if float(math) == 4.00:
            math = 'A'
        elif float(math) < 4.00 and float(math) > 3.49:
            math = 'B+'
        elif float(math) < 3.50 and float(math) > 2.99:
            math = 'B'
        elif float(math) < 3.00 and float(math) > 2.49:
            math = 'C+'
        elif float(math) < 2.50 and float(math) > 1.99:
            math = 'C'
        elif float(math) < 2.00 and float(math) > 1.49:
            math = 'D+'
        elif float(math) < 1.50 and float(math) > 0.99:
            math = 'D'
        elif float(math) < 1.00:
            math = 'F'
        sci = request.POST.get('sci')
        if float(sci) == 4.00:
            sci = 'A'
        elif float(sci) < 4.00 and float(sci) > 3.49:
            sci = 'B+'
        elif float(sci) < 3.50 and float(sci) > 2.99:
            sci = 'B'
        elif float(sci) < 3.00 and float(sci) > 2.49:
            sci = 'C+'
        elif float(sci) < 2.50 and float(sci) > 1.99:
            sci = 'C'
        elif float(sci) < 2.00 and float(sci) > 1.49:
            sci = 'D+'
        elif float(sci) < 1.50 and float(sci) > 0.99:
            sci = 'D'
        elif float(sci) < 1.00:
            sci = 'F'
        society = request.POST.get('society')
        if float(society) == 4.00:
            society = 'A'
        elif float(society) < 4.00 and float(society) > 3.49:
            society = 'B+'
        elif float(society) < 3.50 and float(society) > 2.99:
            society = 'B'
        elif float(society) < 3.00 and float(society) > 2.49:
            society = 'C+'
        elif float(society) < 2.50 and float(society) > 1.99:
            society = 'C'
        elif float(society) < 2.00 and float(society) > 1.49:
            society = 'D+'
        elif float(society) < 1.50 and float(society) > 0.99:
            society = 'D'
        elif float(society) < 1.00:
            society = 'F'
        hygiene = request.POST.get('hygiene')
        if float(hygiene) == 4.00:
            hygiene = 'A'
        elif float(hygiene) < 4.00 and float(hygiene) > 3.49:
            hygiene = 'B+'
        elif float(hygiene) < 3.50 and float(hygiene) > 2.99:
            hygiene = 'B'
        elif float(hygiene) < 3.00 and float(hygiene) > 2.49:
            hygiene = 'C+'
        elif float(hygiene) < 2.50 and float(hygiene) > 1.99:
            hygiene = 'C'
        elif float(hygiene) < 2.00 and float(hygiene) > 1.49:
            hygiene = 'D+'
        elif float(hygiene) < 1.50 and float(hygiene) > 0.99:
            hygiene = 'D'
        elif float(hygiene) < 1.00:
            hygiene = 'F'
        art = request.POST.get('art')
        if float(art) == 4.00:
            art = 'A'
        elif float(art) < 4.00 and float(art) > 3.49:
            art = 'B+'
        elif float(art) < 3.50 and float(art) > 2.99:
            art = 'B'
        elif float(art) < 3.00 and float(art) > 2.49:
            art = 'C+'
        elif float(art) < 2.50 and float(art) > 1.99:
            art = 'C'
        elif float(art) < 2.00 and float(art) > 1.49:
            art = 'D+'
        elif float(art) < 1.50 and float(art) > 0.99:
            art = 'D'
        elif float(art) < 1.00:
            art = 'F'
        career = request.POST.get('career')
        if float(career) == 4.00:
            career = 'A'
        elif float(career) < 4.00 and float(career) > 3.49:
            career = 'B+'
        elif float(career) < 3.50 and float(career) > 2.99:
            career = 'B'
        elif float(career) < 3.00 and float(career) > 2.49:
            career = 'C+'
        elif float(career) < 2.50 and float(career) > 1.99:
            career = 'C'
        elif float(career) < 2.00 and float(career) > 1.49:
            career = 'D+'
        elif float(career) < 1.50 and float(career) > 0.99:
            career = 'D'
        elif float(career) < 1.00:
            career = 'F'
        langues = request.POST.get('langues')
        if float(langues) == 4.00:
            langues = 'A'
        elif float(langues) < 4.00 and float(langues) > 3.49:
            langues = 'B+'
        elif float(langues) < 3.50 and float(langues) > 2.99:
            langues = 'B'
        elif float(langues) < 3.00 and float(langues) > 2.49:
            langues = 'C+'
        elif float(langues) < 2.50 and float(langues) > 1.99:
            langues = 'C'
        elif float(langues) < 2.00 and float(langues) > 1.49:
            langues = 'D+'
        elif float(langues) < 1.50 and float(langues) > 0.99:
            langues = 'D'
        elif float(langues) < 1.00:
            langues = 'F'
        if form.is_valid():
            user_input: UserPredict = form.save(commit=False)
            user_input.user = request.user
            user_input.save()
        #create data frame for data user input 
        df_new = pd.DataFrame({
            'major': [major],
            'admission_grade': [admission_grade],
            'gpa_year_1': [gpa_year_1],
            'thai': [thai],
            'math': [math],
            'sci': [sci],
            'society': [society],
            'hygiene': [hygiene],
            'art': [art],
            'career': [career],
            'langues': [langues]
        })            
        
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

            print(cv_data['test_score'])#ดูเปอร์เซ็นต์ความถูกต้องของแต่ละรอบที่ทำ cross validation
            acc = cv_data['test_score'].mean()
            acc2 = round(acc*100, 2)
            print(cv_data['test_score'].mean())

            pipe.fit(X, y)#model
            result = pipe.predict(df_new)#predict
            result2 = result[0]
            return render(request, 'app_prediction/prediction_result.html', {'result': result2, 'acc': acc2})
                
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

            print(cv_data['test_score'])#ดูเปอร์เซ็นต์ความถูกต้องของแต่ละรอบที่ทำ cross validation
            acc = cv_data['test_score'].mean()
            acc2 = round(acc*100, 2)
            print(cv_data['test_score'].mean())

            pipe.fit(X, y)#model
            result = pipe.predict(df_new)#predict
            result2 = result[0]
            return render(request, 'app_prediction/prediction_result.html', {'result': result2, 'acc': acc2})
        
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

            print(cv_data['test_score'])#ดูเปอร์เซ็นต์ความถูกต้องของแต่ละรอบที่ทำ cross validation
            acc = cv_data['test_score'].mean()
            acc2 = round(acc*100, 2)
            print(cv_data['test_score'].mean())

            pipe.fit(X, y)#model
            result = pipe.predict(df_new)#predict
            result2 = result[0]
            return render(request, 'app_prediction/prediction_result.html', {'result': result, 'acc': acc2})
        
        else:
            print("ไม่เข้าเงื่อนไข")
    return render(request, 'app_prediction/prediction_result.html')
    

@login_required
def information(request):
    data = UserPredict.objects.all()
    total = data.count() 
    print(total)
    context={
      'data': data,
      'total': total,
    } 
    return render(request, 'app_prediction/show_data_input.html', context)

@login_required
def result(request):
    return render(request, 'app_prediction/prediction_result.html')