from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from app_users.forms import *
from .models import User
from app_prediction.models import UserForecasts
from app_prediction.forms import *
from app_demo_model.models import *
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
def check_admin(user):
    return user.is_superuser or user.is_staff

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "ลงทะเบียนเข้าใช้งานสำเร็จแล้ว")
    
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "app_users/register.html", context)

@login_required
def show_profile(request):
    user = request.user
    print('user = ', user)
    form = TeacherForm()
    fil_user = User.objects.filter(username=user)
    print('fil user = ', fil_user)    
    context = {
        'form': form,
    }
    return render(request, "app_users/profile.html", context)

@login_required
def update_profile(request):
    user = request.user
    print(user)
    print('user = ', user)
    form = UpdateProfileForm()
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            form = UpdateProfileForm(request.POST, instance=user)
    context = {
        'form': form,
    }
    return render(request, 'app_users/update_profile.html', context)

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
    data = UserForecasts.objects.filter(user_id=user0).order_by('-predict_at')
    # filter_user_id = data
    total = data.count()
    context = {
        'data': data,
        'total': total,
    }
    return render(request, 'app_users/my_history.html', context)

@login_required
def history_item(request, id):
    data = UserForecasts.objects.filter(id=id)
    print(data)
    context = {
        'item': data
    }
    return render(request, 'app_users/my_history.html', context)

@login_required
@user_passes_test(check_admin, login_url='error_page')
def add_teacher(request):
    branch = Branch.objects.all().values()
    form = TeacherForm()
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_teacher = True
            user.save()
            return HttpResponseRedirect(reverse('view_teacher'))
    context = {
        'form': form,
        'branch': branch,
    }
    return render(request, 'app_users/add_teacher.html', context)

@login_required
@user_passes_test(check_admin, login_url='error_page')
def update_teacher(request, id):
    user_fil = User.objects.get(id=id)
    form = UpdateTeacherForm()
    branch = Branch.objects.all()
    if request.method == 'POST':
        form = UpdateTeacherForm(request.POST, instance=user_fil)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_teacher'))
        else:
            form = UpdateTeacherForm(request.POST, instance=user_fil)
    context = {
        'form': form,
        'user_fil': user_fil,
        'branch': branch,
    }
    return render(request, 'app_users/update_teacher.html', context)

@login_required
@user_passes_test(check_admin, login_url='error_page')
def view_teacher(request):
    teacher = User.objects.filter(is_teacher=True)
    teacher_total = teacher.count()
    
    context = {
        'teacher': teacher,
        'teacher_total': teacher_total,
    }
    return render(request, 'app_users/teacher.html', context)

@login_required
@user_passes_test(check_admin, login_url='error_page')
def delete_teacher(request, id):
    teacher = User.objects.filter(id=id)
    teacher.delete()
    return HttpResponseRedirect(reverse('view_teacher'))
    