from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from .utils import generate_password
from django.contrib import messages
from django.db import IntegrityError
from base.models import Employee, Profile, Leave, SalaryAdvance
from notification.views import (
    
    send_mail_new_employee,
    VetLeaveNotification

)



def user_management(request):
    get_user_count = User.objects.all().count()


    get_user_obj = User.objects.select_related('profile').all()
    
    context = {        
        'get_user_count': get_user_count,
        'get_user_obj': get_user_obj,
    }
    return render(request, 'admin_users/user_management.html', context)


def add_employee(request):
    return render(request, 'admin_users/add-employee.html')

def create_employee(request):
    if request.method == 'POST':

        password = generate_password(6)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        employment_type = request.POST.get('employment_type')
        position = request.POST.get('position')
        employment_status = request.POST.get('employment_status')
        salary_amount = request.POST.get('salary_amount')
        currency = request.POST.get('currency')
        get_department = request.POST.get('department')
        new_department = get_department.upper()



        checK_email = User.objects.filter(email=email).exists()
        if checK_email:
            messages.error(request, "Email already exists!")
            return redirect('admin_users:user_management')

        print(password, first_name, last_name, email, employment_type, position, employment_status, salary_amount, currency, new_department)

        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        
        get_same_user = User.objects.get(email=email)

        create_employee = Employee.objects.create(user=get_same_user, employment_type=employment_type, position=position, employment_status=employment_status, salary_amount=salary_amount, currency=currency)

        add_user_to_department = Profile.objects.get(user=user)
        add_user_to_department.department = new_department
        add_user_to_department.save()

        send_mail_new_employee(email, password)
    
        messages.success(request, "Employee added successfully!")
        return redirect('admin_users:user_management')



def leave_request(request):
    leaves = Leave.objects.all()  
    context = {
        'leaves': leaves,
    }


    return render(request, 'admin_users/leave_request.html', context)


def salary_advance_request(request):
    salary_advc = SalaryAdvance.objects.all()

    context = {
        'salary_advc':salary_advc
    }
    return render(request, 'admin_users/salary_advance_request.html', context)


def vett_salary_advc_request(request, id):
    if request.method == 'POST':
        get_action = request.POST.get("action")
        salary_adv = get_object_or_404(SalaryAdvance, id=id)
        salary_adv.approval_status = get_action
        salary_adv.save()
    else:
        messages.warning(request, "Invalid action",)
        return redirect('admin_users:salary_advance_request')
    
    return redirect('admin_users:salary_advance_request')



def vett_leave_request(request, id):
    if request.method == 'POST':
        get_action = request.POST.get("action")
        leave_req = get_object_or_404(Leave, id=id)
        
        leave_req.status = get_action
        leave_req.save()
        leave_obj = VetLeaveNotification(leave_req.id, get_action)
        leave_obj.send_mail_application()
    else:
        messages.warning(request, "Invalid action",)
        return redirect('admin_users:leave_request')
    
    return redirect('admin_users:leave_request')

    

        
       
