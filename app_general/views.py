from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

# Create your views here.
def dashboard(request):
    return render(request, 'app_general/dashboard.html')