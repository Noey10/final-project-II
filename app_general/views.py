from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
import pandas as pd
from app_prediction.models import UserPredict

# Create your views here.
@login_required
def dashboard(request):
    data = UserPredict
    item = data.objects.all()

    total = item.count()
    print('total = ', total)
    
    all_pass = data.objects.filter(status='Pass').count()
    all_fail = data.objects.filter(status='Fail').count()
    print(all_pass, ', ', all_fail)
    
    
    ict_pass = data.objects.filter(major='ICT').filter(status='Pass').count()
    ict_fail = data.objects.filter(major='ICT').filter(status='Fail').count()

    dssi_pass = data.objects.filter(major='DSSI').filter(status='Pass').count()
    dssi_fail = data.objects.filter(major='DSSI').filter(status='Fail').count()
    
    polymer_pass = data.objects.filter(major='polymer').filter(status='Pass').count()
    polymer_fail = data.objects.filter(major='polymer').filter(status='Fail').count()
    
    enviSci_pass = data.objects.filter(major='enviSci').filter(status='Pass').count()
    enviSci_fail = data.objects.filter(major='enviSci').filter(status='Fail').count()
    
    safety_pass = data.objects.filter(major='safety').filter(status='Pass').count()
    safety_fail = data.objects.filter(major='safety').filter(status='Fail').count()
    
    math_pass = data.objects.filter(major='math').filter(status='Pass').count()
    math_fail = data.objects.filter(major='math').filter(status='Fail').count()
    
    bio_pass = data.objects.filter(major='bio').filter(status='Pass').count()
    bio_fail = data.objects.filter(major='bio').filter(status='Fail').count()
    
    microBio_pass = data.objects.filter(major='microBio').filter(status='Pass').count()
    microBio_fail = data.objects.filter(major='microBio').filter(status='Fail').count()
    
    chemi_pass = data.objects.filter(major='chemi').filter(status='Pass').count()
    chemi_fail = data.objects.filter(major='chemi').filter(status='Fail').count()
    
    physics_pass = data.objects.filter(major='physics').filter(status='Pass').count()
    physics_fail = data.objects.filter(major='physics').filter(status='Fail').count()
    #
    status_pass = [
        dssi_pass,
        ict_pass,
        polymer_pass,
        enviSci_pass,
        safety_pass,
        bio_pass,
        chemi_pass,
        math_pass,
        microBio_pass,
        physics_pass
    ]
    
    status_fail = [
        dssi_fail,
        ict_fail,
        polymer_fail,
        enviSci_fail,
        safety_fail,
        bio_fail,
        chemi_fail,
        math_fail,
        microBio_fail,
        physics_fail
    ]
    #
    admission_grade = data.objects.filter(admission_grade__lt =2.00).count()
    admission_grade2 = data.objects.filter(admission_grade__gte =2.00).count()
    
    gpa = data.objects.filter(gpa_year_1__lt =2.00).count()
    gpa2 = data.objects.filter(gpa_year_1__gte =2.00).count()
    
    thai = data.objects.filter(thai__lt =2.00).count()
    thai2 = data.objects.filter(thai__gte =2.00).count()
    
    math = data.objects.filter(math__lt =2.00).count()
    math2 = data.objects.filter(math__gte =2.00).count()
    
    sci = data.objects.filter(sci__lt =2.00).count()
    sci2 = data.objects.filter(sci__gte =2.00).count()
    
    society = data.objects.filter(society__lt =2.00).count()
    society2 = data.objects.filter(society__gte =2.00).count()
    
    hygiene = data.objects.filter(hygiene__lt =2.00).count()
    hygiene2 = data.objects.filter(hygiene__gte =2.00).count()
    
    art = data.objects.filter(art__lt =2.00).count()
    art2 = data.objects.filter(art__gte =2.00).count()
    
    career = data.objects.filter(career__lt =2.00).count()
    career2 = data.objects.filter(career__gte =2.00).count()
    
    langues = data.objects.filter(langues__lt =2.00).count()
    langues2 = data.objects.filter(langues__gte =2.00).count()
    
    subject_more_than_two = [
        admission_grade,
        gpa,
        thai,
        math,
        sci,
        society,
        hygiene,
        art,
        career,
        langues,
    ]
    
    subject_less_than_two = [
        admission_grade2,
        gpa2,
        thai2,
        math2,
        sci2,
        society2,
        hygiene2,
        art2,
        career2,
        langues2,
    ]
    print('มากกว่า 2', subject_more_than_two)
    print('น้อยกว่า 2', subject_less_than_two)

    per_pass = round((all_pass/total)*100, 2)
    per_fail = round((all_fail/total)*100, 2)
    
    context = {
        'item': item,
        'total': total,
        'all_pass': all_pass,
        'all_fail': all_fail,
        'status_pass': status_pass,
        'status_fail': status_fail,
        'subject_more_than_two': subject_more_than_two,
        'subject_less_than_two': subject_less_than_two,
        'per_pass': per_pass,
        'per_fail': per_fail,
    }
    return render(request, 'app_general/dashboard.html', context)