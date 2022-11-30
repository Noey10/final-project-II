from django.shortcuts import render
from app_prediction.forms import PredictionForm
from app_prediction.models import Prediction
from django.urls import reverse
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect



# Create your views here.
def prediction(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_predict = Prediction()
            new_predict.gender = data['gender']
            new_predict.plan_highschool = data['plan_highschool']
            new_predict.highschool_grade = data['highschool_grade']
            new_predict.professional_grade = data['professional_grade']
            new_predict.compulsory_pro_grade = data['compulsory_pro_grade']
            new_predict.select_vocation_grade = data['select_vocation_grade']
            new_predict.compulsory_elective_1 = data['compulsory_elective_1']
            new_predict.compulsory_elective_2 = data['compulsory_elective_2']
            new_predict.foreign_language_grade = data['foreign_language_grade']
            new_predict.thai_grade = data['thai_grade']
            new_predict.avg_grade = data['avg_grade']
            new_predict.result_predict = data['result_predict']        
            print(data)
            new_predict.save()
        return HttpResponseRedirect(reverse('result'))
    form = PredictionForm()
    context = {'form': form}
    return render(request, 'app_general/prediction_form.html', context)

def result(request):
    return render(request, 'app_general/prediction_result.html')