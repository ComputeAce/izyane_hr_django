from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='/login')
def home(request):
    return render(request, 'base/home.html')


def login(request):
    if request.method == "POST":
        user_username = request.POST.get('email')
        user_password = request.POST.get('password')
        user = authenticate(request, username=user_username, password=user_password)

        if user is not None:
          
            auth_login(request, user)
            return redirect('base:home') 
        else:

            messages.warning(request, 'Invalid credentials')
            return render(request, 'base/login.html')

    return render(request, 'base/login.html')


def add_employee(request):
    return "Added"


def user_profile(request):
    
    return render(request, 'base/profile.html')


def user_settings(request):
    return render(request, 'base/user_settings.html')
