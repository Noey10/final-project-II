from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app_users.forms import ExtendedProfileForm, RegisterForm, UserProfileForm
from app_prediction.models import UserPredict
from app_prediction.forms import *
from app_demo_model.models import *
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "ลงทะเบียนเข้าใช้งานสำเร็จแล้ว")
    
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
def my_dashboard(request):
    user0 = request.user.id
    user1 = request.user
    print('user id = ', user0)
    
    context = {
        'user': user1,
    }
    return render(request, 'app_users/my_dashboard.html', context)


@login_required
def my_history(request):
    user0 = request.user.id
    data = UserPredict
    filter_user_id = data.objects.filter(user_id=user0).order_by('-predict_at')
    total = filter_user_id.count()
    
    #Pagination
    page = Paginator(filter_user_id, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    
    context = {
        'filter_user_id': filter_user_id,
        'total': total,
        'page': page,
    }
    
    return render(request, 'app_users/my_history.html', context)


def history_item(request, id):
    data = UserPredict.objects.filter(id=id)
    print(data)
    context = {
        'item': data
    }
    
    return render(request, 'app_users/my_history.html', context)

    
    
    
    