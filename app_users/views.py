from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app_users.forms import ExtendedProfileForm, RegisterForm, UserProfileForm
from app_prediction.models import UserPredict
from app_users.models import CustomUser
from app_prediction.forms import *
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("login"))
    
    else:
        form = RegisterForm()
    
    context = {"form": form}
    return render(request, "app_users/register.html", context)

@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        is_new_profile = False
        
        try:
            #update
            extended_form = ExtendedProfileForm(request.POST, instance=user.profile)
        except:
            #create
            extended_form = ExtendedProfileForm(request.POST)
            is_new_profile = True
            
        if form.is_valid() and extended_form.is_valid():
            form.save()
            
            if is_new_profile:
                #create
                profile = extended_form.save(commit=False)
                profile.user = user
                profile.save()
            else:
                #update
                extended_form.save()
                
            messages.success(request, "อัปเดตข้อมูลสำเร็จ")
            return HttpResponseRedirect(reverse('profile'))
        
    else:
        form = UserProfileForm(instance=user)
        try:
            extended_form = ExtendedProfileForm(instance=user.profile)
        except:
            extended_form = ExtendedProfileForm()
        
    context = {
        "form": form,
        "extended_form": extended_form
    }
    
    return render(request, "app_users/profile.html", context)

@login_required
def my_history(request):
    user0 = request.user.id
    print(user0)
    data = UserPredict
    filter_user_id = data.objects.filter(user_id=user0).values().order_by('-predict_at')
    
    total = filter_user_id.count()
    
    context = {
        'filter_user_id': filter_user_id,
        'total': total,
    }
    
    return render(request, 'app_users/my_history.html', context)

@login_required
def my_dashboard(request):
    user0 = request.user.id
    user1 = request.user
    print('user id = ', user0)
    data = UserPredict
    filter_user_id = data.objects.filter(user_id=user0).values().order_by('-predict_at')
    total = filter_user_id.count()
    status_pass = filter_user_id.filter(status='Pass').count()
    status_fail = filter_user_id.filter(status='Fail').count()
    print(total, status_pass, status_fail)
    
    context = {
        'filter': filter_user_id,
        'total': total,
        'pass': status_pass,
        'fail': status_fail,
        'user': user1,
    }
    return render(request, 'app_users/my_dashboard.html', context)

@login_required
def update_predict(request, id):
    if request.method == 'POST':
        data = UserPredict.objects.get(id=id)
        form = UserPredictForm(instance=data)
        
    context = {
        'form': form,
        
    }
    return render(request, 'app_prediction/prediction_form.html', context)


