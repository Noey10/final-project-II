from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import Grades
import pandas as pd


def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:      
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)          
        empexceldata = pd.read_excel(filename)        
        dbframe = empexceldata
        for dbframe in dbframe.itertuples():
            obj = Grades.objects.create(major=dbframe.major, 
                                        gpa=dbframe.gpa,
                                        admission_grade=dbframe.admission_grade,
                                        gpa_year_1=dbframe.gpa_year_1,
                                        thai=dbframe.thai,
                                        mathematics=dbframe.mathematics,
                                        science=dbframe.science,
                                        society=dbframe.society,
                                        hygiene=dbframe.hygiene,
                                        art=dbframe.art,
                                        career=dbframe.career,
                                        english=dbframe.english,
                                        status=dbframe.status, 
                                        )           
            print(obj)
            obj.save()
            
    return render(request, 'app_demo_model/form.html')