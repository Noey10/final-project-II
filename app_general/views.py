from django.urls import reverse
from django.shortcuts import render
from app_prediction.models import UserForecasts
from app_users.models import User
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
    return user.is_staff or user.is_teacher

@login_required
@user_passes_test(check_user, login_url='my_dashboard')
def dashboard(request):
    user = request.user
    item = UserForecasts.objects.all()
    branch = Branch.objects.all()
    data =  item.filter(user__is_superuser=True) | item.filter(user__is_teacher=True)
        
    total = data.count()
    print('total = ', total)
    
    my_list = []
    
    for i in branch:
        branch_i = i.abbreviation
        try:
            total_branch = data.filter(branch__abbreviation__icontains=branch_i).count()
            total_branch_percent = round((total_branch/total)*100, 2)
            pass_branch = data.filter(branch__abbreviation__icontains=branch_i, status='Pass').count()
            fail_branch = data.filter(branch__abbreviation__icontains=branch_i, status='Fail').count()
            branch_pass_percent = round((pass_branch/total_branch)*100, 2)
            branch_fail_percent = round((fail_branch/total_branch)*100, 2)
        except:
            total_branch = 0
            total_branch_percent = 0
            pass_branch = 0
            fail_branch = 0
            branch_pass_percent = 0
            branch_fail_percent = 0
        my_list.append([branch_i, total_branch, total_branch_percent, pass_branch, fail_branch, branch_pass_percent, branch_fail_percent])
    
    df = pd.DataFrame(my_list, columns=['branch', 'total', 'amount', 'total_pass', 'total_fail', 'percentage_pass', 'percentage_fail'])
    
    my_dict = df.to_dict('records')
    
    try: 
        total_pass = data.filter(status='Pass').count()
        per_pass = round((total_pass/total)*100, 2)
        # print('percentage pass = ', per_pass)
        total_fail = data.filter(status='Fail').count()
        per_fail = round((total_fail/total)*100, 2)
        # print('percentage pass = ', per_fail)
    except:
        total_pass = 0
        per_pass = 0
        total_fail = 0
        per_fail = 0
        

    context = {
        'data': data,
        'total': total,
        'total_pass': total_pass,
        'per_pass': per_pass,
        'per_fail': per_fail,
        'total_fail': total_fail,
        'mydict': my_dict,
    }
    
    return render(request, 'app_general/dashboard.html', context)

def about_model(request):       
    return render(request, 'app_general/about_model.html')

def error_page(request):  
    return render(request, 'app_general/errors_page.html')
