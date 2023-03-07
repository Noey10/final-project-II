from django.urls import reverse
from django.shortcuts import render
from app_prediction.models import UserPredict
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import pandas as pd
import numpy as np
from django.core.paginator import Paginator
from app_demo_model.models import *
from app_demo_model.resources import *
from django.contrib import messages
from tablib import Dataset

# Create your views here.
def check_user(user):
    return user.is_staff

@login_required
@user_passes_test(check_user, login_url='my_dashboard')
def dashboard(request):
    data = UserPredict
    item = data.objects.all()
    total = item.count()
    print('total = ', total)  
        
    all_pass = data.objects.filter(status='Pass').count()
    all_fail = data.objects.filter(status='Fail').count()
    print('pass:', all_pass, ', ', 'fail:', all_fail)
    
    branch = Branch.objects.all()
    status_pass = []
    status_fail =[]
    for i in branch:
        b_status_p =  data.objects.filter(branch=i, status='Pass').count()
        status_pass.append(b_status_p)
        
        b_status_f =  data.objects.filter(branch=i, status='Fail').count()
        status_fail.append(b_status_f)
    
    per_pass = 0
    per_fail = 0
    if not all_pass == 0 :
        per_pass = round((all_pass/total)*100, 2)
        per_fail = round((all_fail/total)*100, 2)
        
    context = {
        'item': item,
        'branch': branch, 
        'total': total,
        'all_pass': all_pass,
        'all_fail': all_fail,
        'per_pass': per_pass,
        'per_fail': per_fail,
        'status_pass': status_pass,
        'status_fail': status_fail,
    }
    
    return render(request, 'app_general/dashboard.html', context)


def error_page(request):  
    return render(request, 'app_general/errors_page.html')

    