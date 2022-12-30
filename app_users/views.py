from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app_users.forms import ExtendedProfileForm, RegisterForm, UserProfileForm


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
    
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