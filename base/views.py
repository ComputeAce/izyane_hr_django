from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages


@login_required(login_url='/login')
def home(request):
    return render(request, 'base/home.html')


from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile

def login(request):
    if request.method == "POST":
        user_username = request.POST.get('email')
        user_password = request.POST.get('password')
        user = authenticate(request, username=user_username, password=user_password)

        if user is not None:
            auth_login(request, user)

            try:
                user_profile = Profile.objects.get(user=user)

                if user_profile.department == "IT":

                    return redirect("employees:employee_dashboard")
                
                """ 
                if user_profile.position == "Manager":

                    return redirect("admin_users:dashboard")
                
               

                elif user_profile.position == "Developer":

                    return redirect("developer:dashboard")
                
                elif user_profile.position == "HR":
                    return redirect("hr:dashboard")
                
                elif user_profile.position == "Sales":
                    return redirect("sales:dashboard")
                
                elif user_profile.position == "Admin":
                    return redirect("admin:dashboard")
                else:
                    return redirect("base:home") 
                """
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found for this user.")
                return render(request, "base/login.html")

        else:
            messages.warning(request, "Invalid credentials")
            return render(request, "base/login.html")

    return render(request, "base/login.html")


def add_employee(request):
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        employment_type = request.POST.get('employment_type')
        position = request.POST.get('position')
        employment_status = request.POST.get('employment_status')
        salary_amount = request.POST.get('salary_amount')
        currency = request.POST.get('currency')
        user = User.objects.create_user(username=email, email=email, password='password')
        return HttpResponse("Employee added successfully!")
    
    return HttpResponse("Invalid request!")

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
    if request.method == 'POST':
        get_current_password = request.POST.get('new_password')
        get_new_password = request.POST.get('current_password')
        get_confirm_password = request.POST.get('confirm_password')

        username = request.user.username
        user =  authenticate(request, username=username, password=get_current_password)
        if user is not None:
            if get_new_password != get_confirm_password:
                messages.warning(request, "Password does not match!")
                return redirect('base:user_settings')
            
            user.set_password(get_new_password)
            user.save()

            messages.info(request, "Password changed successfully!")
            logout(request)
            return redirect('base:login')
        else:
            messages.warning(request, "Invalid current password!")
            return redirect('base:user_settings')

    return render(request, 'base/user_settings.html')



def view_employee(request):
    return render(request, 'base/employee.html')

def logout_user(request):
    logout(request)
    return redirect('base:login')