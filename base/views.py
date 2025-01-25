from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
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



@login_required
def user_profile(request):
    if request.method == 'POST':
        get_username = request.POST.get('username')
        get_first_name = request.POST.get('first_name')
        get_last_name = request.POST.get('last_name')
        get_email = request.POST.get('email')

        print(get_username, get_first_name, get_last_name, get_email)

        errors = []

        if not get_first_name:
            errors.append("First name is required.")
        if not get_last_name:
            errors.append("Last name is required.")
        if not get_email:
            errors.append("Email is required.")

        try:
            if get_email:
                validate_email(get_email)
        except ValidationError:
            errors.append("Invalid email format.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('base:user_profile')

        user_obj = User.objects.get(id=request.user.id)

        if user_obj:
            if user_obj.first_name != get_first_name:
                user_obj.first_name = get_first_name
            if user_obj.last_name != get_last_name:
                user_obj.last_name = get_last_name
            if user_obj.email != get_email:
                user_obj.email = get_email
                
            user_obj.save() 

        messages.success(request, "Profile updated successfully!")
        return redirect('base:user_profile')
    return render(request, 'base/profile.html')








def user_settings(request):
    return render(request, 'base/user_settings.html')
