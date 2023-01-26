from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
import pandas as pd
from app_prediction.models import UserPredict

# Create your views here.
def dashboard(request):
    data = UserPredict
    item = data.objects.all()

    total = item.count()
    print('total = ', total)
    
    #จำนวนทำนายผลเป็น PASS, FAIL
    status_pass = data.objects.filter(status='Pass').count()
    print('status pass = ', status_pass)
    status_fail = data.objects.filter(status='fail').count()
    print('status fail = ', status_fail)
    print('-----------------------------------------------------------')
    #จำนวนทำนายผลเป็น PASS, FAIL ของแต่ละสาขา
    ict_pass = data.objects.filter(major='ICT').filter(status='Pass').count()
    ict_fail = data.objects.filter(major='ICT').filter(status='Fail').count()
    print('ict pass = ', ict_pass)
    print('ict fail = ', ict_fail)

    dssi_pass = data.objects.filter(major='DSSI').filter(status='Pass').count()
    dssi_fail = data.objects.filter(major='DSSI').filter(status='Fail').count()
    print('dssi pass = ', dssi_pass)
    print('dssi fail = ', dssi_fail)
    
    polymer_pass = data.objects.filter(major='polymer').filter(status='Pass').count()
    polymer_fail = data.objects.filter(major='polymer').filter(status='Fail').count()
    print('polymer pass = ', polymer_pass)
    print('polymer fail = ', polymer_fail)
    
    enviSci_pass = data.objects.filter(major='enviSci').filter(status='Pass').count()
    enviSci_fail = data.objects.filter(major='enviSci').filter(status='Fail').count()
    print('environment sci pass = ', enviSci_pass)
    print('environment sci fail = ', enviSci_fail)
    
    safety_pass = data.objects.filter(major='safety').filter(status='Pass').count()
    safety_fail = data.objects.filter(major='safety').filter(status='Fail').count()
    print('safety pass = ', safety_pass)
    print('safety fail = ', safety_fail)
    
    math_pass = data.objects.filter(major='math').filter(status='Pass').count()
    math_fail = data.objects.filter(major='math').filter(status='Fail').count()
    print('math pass = ', math_pass)
    print('math fail = ', math_fail)
    
    bio_pass = data.objects.filter(major='bio').filter(status='Pass').count()
    bio_fail = data.objects.filter(major='bio').filter(status='Fail').count()
    print('bio pass = ', bio_pass)
    print('bio fail = ', bio_fail)
    
    microBio_pass = data.objects.filter(major='microBio').filter(status='Pass').count()
    microBio_fail = data.objects.filter(major='microBio').filter(status='Fail').count()
    print('micro bio pass = ', microBio_pass)
    print('micro bio fail = ', microBio_fail)
    
    chemi_pass = data.objects.filter(major='chemi').filter(status='Pass').count()
    chemi_fail = data.objects.filter(major='chemi').filter(status='Fail').count()
    print('chemi pass = ', chemi_pass)
    print('chemi fail = ', chemi_fail)
    
    physics_pass = data.objects.filter(major='physics').filter(status='Pass').count()
    physics_fail = data.objects.filter(major='physics').filter(status='Fail').count()
    print('physics pass = ', physics_pass)
    print('physics fail = ', physics_fail)
    print('-----------------------------------------------------------')
    #ดูจำนวนเกรดแต่ละวิชาที่มากกกว่า 2 และ น้อยกว่า 2
    thai_grade = data.objects.filter(thai__lt =2.00).values()
    print(thai_grade.count())
    thai_grade2 = data.objects.filter(thai__gte =2.00).values()
    print(thai_grade2.count())
    
    context = {
        'item': item,
    }
    return render(request, 'app_general/dashboard.html', context)