from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from app_prediction.models import Prediction
from app_demo_model.models import GradesInput

# Create your views here.
def information(request):
    all_result = Prediction.objects.all()
    total = Prediction.objects.all().count()
    context = {'results': all_result,
               'total': total
               }
    return render(request, 'app_general/information.html', context)

def dashboard(request: HttpRequest):
    labels = []
    data = []

    queryset = GradesInput.objects.all()
    tot = 0
    tot2 = 0
    
    for item in queryset:
        if item.status == '1':
            tot += 1
        else:
            tot2 += 1
    
    labels.append('True')
    labels.append('False')
    
    data.append(tot)
    data.append(tot2)

    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'app_general/dashboard.html', context)

def profile(request):
    return render(request, 'app_general/profile.html')

def homepage(request):
    return render(request, 'app_general/homepage.html')