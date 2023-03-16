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
    return user.is_staff or user.is_teacher

@login_required
@user_passes_test(check_user, login_url='my_dashboard')
def dashboard(request):
    user = request.user
    user_admin = user.is_superuser
    user_teacher = user.is_teacher
    
    branch = Branch.objects.all()
    data = UserPredict.objects
    total = data.count()
    
    #filter data in Bio
    total_bio = data.filter(branch__abbreviation__icontains='bio').count()
    #filter status pass
    bio_pass = data.filter(branch__abbreviation__icontains='bio', status='Pass').count()
    #filter status fail
    bio_fail = data.filter(branch__abbreviation__icontains='bio', status='Fail').count()
    try:
        #calculate percentage status pass
        bio_pass_percent = round((bio_pass/total_bio)*100, 2)
        #calculate percentage status fail
        bio_fail_percent = round((bio_fail/total_bio)*100, 2)
    except:
        bio_pass_percent = 0
        bio_fail_percent = 0
    
    
    #filter data in Chemi
    total_chemi = data.filter(branch__abbreviation__icontains='chemi').count()
    chemi_pass = data.filter(branch__abbreviation__icontains='chemi', status='Pass').count()
    chemi_fail = data.filter(branch__abbreviation__icontains='chemi', status='Fail').count()
    try:
        chemi_pass_percent = round((chemi_pass/total_chemi)*100, 2)
        chemi_fail_percent = round((chemi_fail/total_chemi)*100, 2)
    except:
        chemi_pass_percent = 0
        chemi_fail_percent = 0
    
    
    #filter data in DSSI
    total_dssi = data.filter(branch__abbreviation__icontains='dssi').count()
    dssi_pass = data.filter(branch__abbreviation__icontains='dssi', status='Pass').count()
    dssi_fail = data.filter(branch__abbreviation__icontains='dssi', status='Fail').count()
    try:
        dssi_pass_percent = round((dssi_pass/total_dssi)*100, 2)
        dssi_fail_percent = round((dssi_fail/total_dssi)*100, 2)
    except: 
        dssi_pass_percent = 0
        dssi_fail_percent = 0
    
    
    #filter data in ICT
    total_ict = data.filter(branch__abbreviation__icontains='ict').count()
    ict_pass = data.filter(branch__abbreviation__icontains='ict', status='Pass').count()
    ict_fail = data.filter(branch__abbreviation__icontains='ict', status='Fail').count()
    try :
        ict_pass_percent = round((ict_pass/total_ict)*100, 2)
        ict_fail_percent = round((ict_fail/total_ict)*100, 2)
    except:
        ict_pass_percent = 0
        ict_fail_percent = 0
    
    
    #คิดเป็นกี่เปอร์เซ็นต์ของข้อมูลทั้งหมดในระบบ
    p_bio = round((total_bio/total)*100, 2)
    p_chemi = round((total_chemi/total)*100, 2)
    p_dssi = round((total_dssi/total)*100, 2)
    p_ict = round((total_ict/total)*100, 2)
    
    myDict = [
        {'branch': 'bio', 'total': total_bio, 'amount': p_bio, 'total_pass': bio_pass, 'total_fail': bio_fail, 'percentage_pass': bio_pass_percent, 'percentage_fail': bio_fail_percent}, 
        {'branch': 'chemi', 'total': total_chemi, 'amount': p_chemi, 'total_pass': chemi_pass, 'total_fail': chemi_fail, 'percentage_pass': chemi_pass_percent, 'percentage_fail': chemi_fail_percent}, 
        {'branch': 'DSSI', 'total': total_dssi, 'amount': p_dssi, 'total_pass': dssi_pass, 'total_fail': dssi_fail, 'percentage_pass': dssi_pass_percent, 'percentage_fail': dssi_fail_percent}, 
        {'branch': 'ICT', 'total': total_ict, 'amount': p_ict, 'total_pass': ict_pass, 'total_fail': ict_fail, 'percentage_pass': ict_pass_percent, 'percentage_fail': ict_fail_percent}, 
    ]
    
    total_pass = data.filter(status='Pass').count()
    per_pass = round((total_pass/total)*100, 2)
    # print('percentage pass = ', per_pass)
    total_fail = data.filter(status='Fail').count()
    per_fail = round((total_fail/total)*100, 2)
    # print('percentage pass = ', per_fail)

    context = {
        'total': total,
        'bio': p_bio,
        'total_pass': total_pass,
        'per_pass': per_pass,
        'per_fail': per_fail,
        'total_fail': total_fail,
        'mydict': myDict,
    }
    
    return render(request, 'app_general/dashboard.html', context)


def error_page(request):  
    return render(request, 'app_general/errors_page.html')

    