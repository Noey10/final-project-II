from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import AppliedScience, HealthScience, PureScience
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def upload_model(request):   
    return render(request, 'app_demo_model/upload_model.html')

@login_required
def upload_applied_sci_model(request):
    if request.method == 'POST':   
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)          
        empexceldata = pd.read_excel(filename)        
        dbframe = empexceldata
        for dbframe in dbframe.itertuples():
            obj = AppliedScience.objects.create(
                major=dbframe.major, 
                admission_grade=dbframe.admission_grade,
                gpa_year_1=dbframe.gpa_year_1,
                thai=dbframe.thai,
                math=dbframe.math,
                sci=dbframe.sci,
                society=dbframe.society,
                hygiene=dbframe.hygiene,
                art=dbframe.art,
                career=dbframe.career,
                langues=dbframe.langues,
                status=dbframe.status, 
            )           
            obj.save()
        messages.success(request, "Upload Applied model successfully.")
            
    return render(request, 'app_demo_model/applied_sci_form_upload_model.html')

@login_required
def upload_health_sci_model(request):
    if request.method == 'POST':   
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)          
        empexceldata = pd.read_excel(filename)        
        dbframe = empexceldata
        for dbframe in dbframe.itertuples():
            obj = HealthScience.objects.create(
                major=dbframe.major, 
                admission_grade=dbframe.admission_grade,
                gpa_year_1=dbframe.gpa_year_1,
                thai=dbframe.thai,
                math=dbframe.math,
                sci=dbframe.sci,
                society=dbframe.society,
                hygiene=dbframe.hygiene,
                art=dbframe.art,
                career=dbframe.career,
                langues=dbframe.langues,
                status=dbframe.status, 
            )           
            obj.save()
            messages.success(request, "Upload Applied model successfully.")
    return render(request, 'app_demo_model/health_sci_form_upload_model.html')

@login_required
def upload_pure_sci_model(request):
    if request.method == 'POST':   
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)          
        empexceldata = pd.read_excel(filename)        
        dbframe = empexceldata
        for dbframe in dbframe.itertuples():
            obj = PureScience.objects.create(
                major=dbframe.major, 
                admission_grade=dbframe.admission_grade,
                gpa_year_1=dbframe.gpa_year_1,
                thai=dbframe.thai,
                math=dbframe.math,
                sci=dbframe.sci,
                society=dbframe.society,
                hygiene=dbframe.hygiene,
                art=dbframe.art,
                career=dbframe.career,
                langues=dbframe.langues,
                status=dbframe.status, 
            )           
            obj.save()
            messages.success(request, "Upload Applied model successfully.")
    return render(request, 'app_demo_model/pure_sci_form_upload_model.html')

@login_required
def data_in_applied_sci(request):
    applied = AppliedScience.objects.all() #for all the records
    total = applied.count() 
    context={
      'applied':applied,
      'total': total,
    } 
    return render(request, 'app_demo_model/data_in_applied_model.html', context)

@login_required
def delete_data_applied(request):
    applied = AppliedScience.objects.all()
    applied.delete()
    return render(request, 'app_demo_model/data_in_applied_model.html')

@login_required
def data_in_health_sci(request):
    applied = HealthScience.objects.all() #for all the records
    total = applied.count() 
    context={
      'applied':applied,
      'total': total,
    } 
    return render(request, 'app_demo_model/data_in_health_model.html')

@login_required
def delete_data_health(request):
    applied = HealthScience.objects.all()
    applied.delete()
    return render(request, 'app_demo_model/data_in_health_model.html')

@login_required
def data_in_pure_sci(request):
    applied = PureScience.objects.all() #for all the records
    total = applied.count() 
    context={
      'applied':applied,
      'total': total,
    } 
    return render(request, 'app_demo_model/data_in_pure_model.html')

@login_required
def delete_data_pure(request):
    applied = PureScience.objects.all()
    applied.delete()
    return render(request, 'app_demo_model/data_in_pure_model.html')
