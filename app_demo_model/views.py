from django.shortcuts import render
import os
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import AppliedScience, HealthScience, PureScience
from .resources import AppliedSciResource, HealthSciResource, PureSciResource
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tablib import Dataset
@login_required
def upload_model(request):   
    return render(request, 'app_demo_model/upload_model.html')

@login_required
def upload_applied_sci_model(request):
    
    if request.method == 'POST':
        applied = AppliedSciResource()
        dataset = Dataset()
        new_applied = request.FILES['appliedfile']
        print('name file = ', new_applied.name)
        
        if not new_applied.name.endswith('xlsx'):
            print('name file gg')
            messages.info(request, 'Wrong format')
            return render(request, 'app_demo_model/applied_sci_form_upload_model.html')
        
        data_import = dataset.load(new_applied.read())
        result = applied.import_data(dataset, dry_run=True)
        if not result.has_errors():
            applied.import_data(dataset, dry_run=False)       
        messages.success(request, "Upload Applied model successfully.")
        
            
    return render(request, 'app_demo_model/applied_sci_form_upload_model.html')

@login_required
def data_in_applied_sci(request):
    applied = AppliedScience.objects.all() #for all the records
    # print(applied)
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
def upload_health_sci_model(request):
    if request.method == 'POST':
        health = HealthSciResource()
        dataset = Dataset()
        new_health = request.FILES['healthfile']
        print('name file = ', new_health.name)
        
        if not new_health.name.endswith('xlsx'):
            print('name file gg')
            messages.info(request, 'Wrong format')
            return render(request, 'app_demo_model/health_sci_form_upload_model.html')
        
        data_import = dataset.load(new_health.read())
        result = health.import_data(dataset, dry_run=True)
        if not result.has_errors():
            health.import_data(dataset, dry_run=False)       
        messages.success(request, "Upload Applied model successfully.")
        
    return render(request, 'app_demo_model/health_sci_form_upload_model.html')

@login_required
def data_in_health_sci(request):
    health = HealthScience.objects.all() #for all the records
    total = health.count() 
    context={
      'health':health,
      'total': total,
    } 
    return render(request, 'app_demo_model/data_in_health_model.html', context)

@login_required
def delete_data_health(request):
    applied = HealthScience.objects.all()
    applied.delete()
    return render(request, 'app_demo_model/data_in_health_model.html')

@login_required
def upload_pure_sci_model(request):
    if request.method == 'POST':
        pure = PureSciResource()
        dataset = Dataset()
        new_pure = request.FILES['purefile']
        print('name file = ', new_pure.name)
        
        if not new_pure.name.endswith('xlsx'):
            print('name file gg')
            messages.info(request, 'Wrong format')
            return render(request, 'app_demo_model/pure_sci_form_upload_model.html')
        
        imported_data = dataset.load(new_pure.read())
        result = pure.import_data(dataset, dry_run=True)
        if not result.has_errors():
            pure.import_data(dataset, dry_run=False)
        
        messages.success(request, 'Upload model successfully.')
        
    return render(request, 'app_demo_model/pure_sci_form_upload_model.html')

@login_required
def data_in_pure_sci(request):
    pure = PureScience.objects.all() #for all the records
    # print(pure)
    total = pure.count() 
    print(total)
    context={
      'pure': pure,
      'total': total,
    } 
    return render(request, 'app_demo_model/data_in_pure_model.html', context)

@login_required
def delete_data_pure(request):
    pure = PureScience.objects.all()
    pure.delete()
    return render(request, 'app_demo_model/data_in_pure_model.html')

@login_required
def show_model(request):
    return render(request, 'app_demo_model/show_model.html')