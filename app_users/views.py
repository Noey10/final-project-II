from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from app_users.forms import RegisterForm


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