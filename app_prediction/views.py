from django.shortcuts import render
from app_prediction.forms import PredictionModelForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def prediction(request):
    if request.method == 'POST':
        form = PredictionModelForm(request.POST)
        if form.is_valid():
           form.save()
        return HttpResponseRedirect(reverse('result'))
    form = PredictionModelForm()
    context = {'form': form}
    return render(request, 'app_prediction/prediction_form.html', context)

@login_required
def result(request):
    return render(request, 'app_prediction/prediction_result.html')