from django.urls import reverse
from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from app_prediction.models import Prediction

# Create your views here.
def home(request):
    return render(request, 'app_general/home.html')

def about(request):
    return render(request, 'app_general/about.html')

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
