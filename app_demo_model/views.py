from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import Grades
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import sklearn.metrics as metrics
import openpyxl
from .resources import GradesResource
from tablib import Dataset

def upload(request):
    if request.method == 'POST':   
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)          
        empexceldata = pd.read_excel(filename)        
        dbframe = empexceldata
        for dbframe in dbframe.itertuples():
            obj = Grades.objects.create(
                # major=dbframe.major, 
                                        gpa=dbframe.gpa,
                                        admission_grade=dbframe.admission_grade,
                                        gpa_year_1=dbframe.gpa_year_1,
                                        thai=dbframe.thai,
                                        mathematics=dbframe.mathematics,
                                        science=dbframe.science,
                                        society=dbframe.society,
                                        hygiene=dbframe.hygiene,
                                        art=dbframe.art,
                                        career=dbframe.career,
                                        english=dbframe.english,
                                        status=dbframe.status, 
                                        )           
            obj.save()
    
    return render(request, 'app_demo_model/form.html')

def test_predict(request):
    return render(request, 'app_demo_model/test_predict.html')

def test(request):
    #read data
    all_data = Grades.objects.all().values()
    df = pd.DataFrame(all_data)
    
    #train-test split data
    features = ['gpa', 'admission_grade', 'gpa_year_1', 'thai', 'mathematics', 'science', 'society', 'hygiene', 'art', 'career', 'english' ]
    X = df[features]
    y = df['status']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    
    #training model
    model = DecisionTreeClassifier()
    model = model.fit(X_train.values, y_train.values)
    
    val1 = float(request.POST['r1'])
    val2 = float(request.POST['r2'])
    val3 = float(request.POST['r3'])
    val4 = float(request.POST['r4'])
    val5 = float(request.POST['r5'])
    val6 = float(request.POST['r6'])
    val7 = float(request.POST['r7'])
    val8 = float(request.POST['r8'])
    val9 = float(request.POST['r9'])
    val10 = float(request.POST['r10'])
    val11 = float(request.POST['r11'])
    
    #prediction
    pred = model.predict([[val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11]])
    print('pred : ', pred)
    result2 = ""
    if pred == ['1']:
        result2 = "True"
    else:
        result2 = "FALSE"
    
    context = {'result2': result2}
    
    return render(request, 'app_prediction/prediction_result.html', context)


def data_in_model(request):
    all_data = Grades.objects.all()
    total_data = Grades.objects.all().count()

    context = {'results2': all_data,
               'total2': total_data
               }
    return render(request, 'app_demo_model/show_data_model.html', context)

def delete_datas(request):
    grades = Grades.objects.all()
    grades.delete()
    return HttpResponseRedirect(reverse('result'))