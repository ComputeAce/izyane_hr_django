from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from base.models import Profile, Employee, Leave, SalaryAdvance, PasswordResetToken
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.core.mail import send_mail



@login_required(login_url='/login')
def home(request):
    total_salary_advc = SalaryAdvance.objects.all().count()
    total_pending_salary_advc = SalaryAdvance.objects.filter(approval_status = 'Pending').count()

    total_leaves = Leave.objects.all().count()
    total_pending_leaves = Leave.objects.filter(status = 'Pending').count()


    get_all_employees = User.objects.all().count()
    get_all_approved_leave = Leave.objects.filter(status = 'Approved').count()
    print("get_all_approved_leave,:", get_all_approved_leave)
    

  

    context = {
        'total_salary_advc': total_salary_advc,
        'total_pending_salary_advc': total_pending_salary_advc,
        'total_leaves': total_leaves,
        'total_pending_leaves': total_pending_leaves,
        'get_all_employees':  get_all_employees,
        'get_all_approved_leave':  get_all_approved_leave
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
                messages.warning(request, "Invalid credentials")
        except User.DoesNotExist:
            messages.warning(request, "Invalid credentials")

    return render(request, "base/login.html")
    
@login_required
def user_profile(request):
    if request.method == 'POST':
        get_first_name = request.POST.get('first_name')
        get_last_name = request.POST.get('last_name')
        get_email = request.POST.get('email')
        get_address = request.POST.get('address')
        get_phone_number = request.POST.get('phone_number')

        errors = []

        if not get_first_name:
            errors.append("First name is required.")
        if not get_last_name:
            errors.append("Last name is required.")
        if not get_email:
            errors.append("Email is required.")
        if not get_address:
            errors.append("Address is required.")

        if not get_phone_number:
            errors.append("Phone number is required")

        try:
            if get_email:
                validate_email(get_email)
        except ValidationError:
            errors.append("Invalid email format.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('base:user_profile')

        user_obj = request.user

        if user_obj:
            user_obj.first_name = get_first_name
            user_obj.last_name = get_last_name
            user_obj.email = get_email
            user_obj.save()

            profile_obj, created = Profile.objects.get_or_create(user=user_obj)
            profile_obj.address = get_address
            profile_obj.phone_number = get_phone_number
            profile_obj.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('base:user_profile')

    return render(request, 'base/profile.html')



def update_profile_img(request):
    if request.method == 'POST' and 'profile_picture' in request.FILES:
    
        image = request.FILES['profile_picture'] 
        user = request.user
        get_profile = Profile.objects.get(user=user)
        get_profile.image = image
        get_profile.save()
        messages.success(request, 'Your profile picture has been updated successfully!')
        return redirect('base:user_profile')  
    
    messages.warning(request, 'Error uploading Your Profile Picture')
    return redirect('base:user_profile')  


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


def forget_password(request):

    if request.method == 'POST':
        get_email = request.POST.get('email')
        user = User.objects.get(email = get_email)
        token = get_random_string(20)

        create_token = PasswordResetToken.objects.create(user = user, token = token)

        reset_url = request.build_absolute_uri(
                reverse('base:reset_forget_password', args=[token])
            )
        send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n{reset_url}',
                'your_email@example.com',
                [get_email],
                fail_silently=False,
            )


        return redirect('base:password_reset_done')
    return render(request, 'base/forget_password.html')


def password_reset_done(request):
    return render(request, 'base/password-reset-done.html')


def reset_forget_password(request, token):
    chek_token_exists = PasswordResetToken.objects.filter(token = token).exists()

    if not chek_token_exists:
        messages.warning(request, 'The reset link has expired. Create a New Request')
        return redirect('base:forget_password')
    
    
    get_password_reset_token =  PasswordResetToken.objects.get(token = token)

    if not get_password_reset_token.is_valid():
        messages.warning(request, 'The reset link has expired. Create a New Request')
        return redirect('base:forget_password')
    
    if request.method == 'POST':
        get_password = request.POST.get('password')
        get_confrim_password = request.POST.get('confrim_password')

        if get_password != get_confrim_password:
            messages.warning(request, 'Passwords does not match. Try again')
            return redirect('base:reset_forget_password', token=token)
        
        get_password_reset_token.user.password = make_password(get_password)
        get_password_reset_token.save()
        get_password_reset_token.delete()
        messages.info(request, 'Your password has been reset successfully. You can login')
        return redirect('base:login')
    
    context = {
        'token': token
    }
        
    return render(request, 'base/reset_forget_password_form.html', context)