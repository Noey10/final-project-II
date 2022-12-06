from django.urls import reverse
from django.shortcuts import render
from app_prediction.models import Prediction

# Create your views here.
def information(request):
    all_result = Prediction.objects.order_by('-predict_at')
    total = Prediction.objects.all().count()
    context = {'results': all_result,
               'total': total
               }
    return render(request, 'app_general/information.html', context)

def dashboard(request):
    return render(request, 'app_general/dashboard.html')

def profile(request):
    return render(request, 'app_general/profile.html')
