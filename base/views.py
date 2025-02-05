from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from base.models import Profile, Employee, Leave, SalaryAdvance
from django.http import JsonResponse



@login_required(login_url='/login')
def home(request):
    get_all_employees = Employee.objects.count()
    get_all_leave_requests = Leave.objects.count()
    get_all_salary_advc_requests = SalaryAdvance.objects.count()
    get_all_approved_leaves = Leave.objects.filter(status = 'Approved').count()
    get_all_rejected_leaves = Leave.objects.filter(status = 'Rejected').count()
    get_all_approved_salary_advc = SalaryAdvance.objects.filter(approval_status = 'Approved').count()
    get_all_rejected_salary_advc = SalaryAdvance.objects.filter(approval_status =  'Rejected').count()
    get_all_users = User.objects.all()

   
    context = {
        'get_all_employees':  get_all_employees,
        'get_all_leave_requests': get_all_leave_requests,
        'get_all_salary_advc_requests': get_all_salary_advc_requests,
        'get_all_users': get_all_users,
        'get_all_approved_leaves': get_all_approved_leaves,
        'get_all_rejected_leaves':  get_all_rejected_leaves,
        'get_all_approved_salary_advc': get_all_approved_salary_advc,
        'get_all_rejected_salary_advc':  get_all_rejected_salary_advc
    }
    return render(request, 'base/home.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)
                return redirect("base:home")
            else:
                messages.error(request, "Invalid credentials")
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials")

    return render(request, "base/login.html")
    

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

def update_profile_img(request):
    if request.method == 'POST' and 'profile_picture' in request.FILES:
    
        image = request.FILES['profile_picture'] 
        user = request.user
        get_profile = Profile.objects.get(user=user)
        get_profile.image = image
        get_profile.save()
        messages.success(request, 'Your profile picture has been updated successfully!')
        return redirect('base:user_profile')  
    
    messages.error(request, 'Failed to update profile picture. Please try again.')
    return redirect('base:user_settings')


def view_employee(request):
    return render(request, 'base/employee.html')

def logout_user(request):
    logout(request)
    return redirect('base:login')


@login_required
def submit_change_password(request):
    if request.method == "POST":
        user = request.user

        get_new_password = request.POST.get('new_password')
        get_current_password = request.POST.get('current_password') 
        
        if not get_new_password:
            return JsonResponse({'error': 'New password is required'}, status=400)
        
        if get_current_password:
        
            user = authenticate(username=user.username, password=get_current_password)
            if not user:
                return JsonResponse({'error': 'Current password is incorrect'}, status=400)

        user.set_password(get_new_password)
        user.save()

        return JsonResponse({'message': 'Password updated successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)



@login_required
def update_password(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        username = request.user.username

        user = authenticate(username=username, password=current_password)
        if user:
            return JsonResponse({
                'status': 'success',
                'message': 'Password is correct',
                'current_password': current_password
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid password',
                'current_password': current_password
            })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
