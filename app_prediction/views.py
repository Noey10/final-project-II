from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def form(request):
    return render(request, 'app_prediction/form_testing_model.html')

@login_required
def information(request):
    return render(request, 'app_prediction/show_data_input.html')

@login_required
def result(request):
    return render(request, 'app_prediction/prediction_result.html')