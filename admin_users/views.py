from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from .utils import generate_password
from django.contrib import messages
from django.db import IntegrityError
from base.models import Employee, Profile, Leave, SalaryAdvance
from notification.views import (
    
    send_mail_new_employee,
    VetLeaveNotification,
    VetSalaryAdvanceNotification,

)




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
        employment_status = 'Active'
        salary_amount = request.POST.get('salary_amount')
        currency = request.POST.get('currency')
        department = request.POST.get('department').upper()
        address = request.POST.get('address')
        id_type = request.POST.get('id_type')
        nhima = request.POST.get('nhima_number')
        ssn = request.POST.get('ssn')
        tpin = request.POST.get('tpin')

        id_front = request.FILES.get('id_front')
        id_back = request.FILES.get('id_back')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('admin_users:create_employee')

        user = User.objects.create_user(
            username=email, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        employee = Employee.objects.create(
            user=user, employment_type=employment_type,
            position=position, employment_status=employment_status,
            salary_amount=salary_amount, currency=currency,
            
        )

        profile = Profile.objects.get(user=user)
        profile.department = department
        profile.address = address
        profile.nhima_number = nhima
        profile.ssn = ssn
        profile.tpin = tpin
        profile.nrc_front = id_front
        profile.nrc_back = id_back
        profile.save()

        send_mail_new_employee(email, password)
        messages.success(request, "Employee added successfully!")
        return redirect('admin_users:add_employee')
    



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
        salary_adv_obj = VetSalaryAdvanceNotification(salary_adv.id, get_action)
        salary_adv_obj.send_mail_application()

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


def all_employee(request):
    all_employees = Employee.objects.all()

    context = {

        'all_employees':all_employees

    }
    return render(request, 'admin_users/view-all-employees.html', context)
    

        
       
