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

        first_name      = request.POST.get('first_name', '').strip()
        last_name       = request.POST.get('last_name', '').strip()
        email           = request.POST.get('email', '').strip()
        employment_type = request.POST.get('employment_type')
        currency = request.POST.get('currency')
        position        = request.POST.get('position')
        salary_amount   = request.POST.get('salary_amount')
        address         = request.POST.get('address')
        id_type         = request.POST.get('id_type')
        nhima          = request.POST.get('nhima_number')
        ssn             = request.POST.get('ssn')
        tpin            = request.POST.get('tpin')
        phone           = request.POST.get('phone')
        id_front        = request.FILES.get('id_front')
        id_back         = request.FILES.get('id_back')

        #print(first_name, last_name, email,  phone , employment_type, position, salary_amount, currency, address, id_type, nhima, ssn, tpin, id_back, id_front)
        
        missing_fields = []

        if not email:
            missing_fields.append("Email")

        if not first_name:
            missing_fields.append("First Name")

        if not last_name:
            missing_fields.append("Last Name")

        if not employment_type:
            missing_fields.append("Employment Type")

        if not position:
            missing_fields.append("Position")

        if missing_fields:
            fields = ", ".join(missing_fields)
            verb = "is" if len(missing_fields) == 1 else "are"
            messages.warning(request, f"{fields} {verb} required!")
            return redirect('admin_users:add_employee')


        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists!")
            return redirect('admin_users:add_employee')

        # Generate a password (assuming generate_password is defined)
        password = generate_password(6)
        
        # Create the User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create the Employee record
        employee = Employee.objects.create(
            user=user,
            employment_type=employment_type,
            position=position,
            employment_status='Active',
            salary_amount=salary_amount,
            currency=currency
        )

        # Determine department based on position using membership test
        if position in ['SOFTWARE DEVELOPER-SNR', 'SOFTWARE DEVELOPER-INTERN', 'TECHNICAL LEAD']:
            department = 'IT'
        elif position in ['TDR', 'CALL CENTER']:
            department = 'CUSTOMER SERVICE'
        elif position in ['CLEANERS', 'DRIVER']:
            department = 'MAINTENANCE'
        elif position in ['ACCOUNTANT', 'OPERATION']:
            department = 'ADMIN'
        else:
            department = None

        # Update the user's profile (assuming a Profile is auto-created or already exists)
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            # Optionally, create a profile if it doesn't exist.
            profile = Profile.objects.create(user=user)
        profile.department  = department
        profile.phone_number =  phone 
        profile.address     = address
        profile.nhima_number = nhima
        profile.ssn         = ssn
        profile.tpin        = tpin
        profile.nrc_front   = id_front
        profile.nrc_back    = id_back
        profile.save()

        # Send credentials via email (assuming send_mail_new_employee is defined)
        send_mail_new_employee(email, password)
        
        messages.success(request, "Employee added successfully!")
        return redirect('admin_users:add_employee')
    
    messages.success(request, "Error, try again")
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


#ALL LEAVE FUNCTIONS


#Pending 
def pending_leaves(request):

    get_all_pending_leave = Leave.objects.filter(status='Pending')
    print(get_all_pending_leave)

    context = {
        'get_all_pending_leave': get_all_pending_leave, 
    }
    return render(request, 'admin_users/leaves/pending-leaves.html', context)


def approved_leaves(request):

    get_all_approved_leave = Leave.objects.filter(status='Approved')
  

    context = {
        'get_all_approved_leave': get_all_approved_leave, 
    }
    return render(request, 'admin_users/leaves/approved-leaves.html', context)



def rejected_leaves(request):

    get_all_rejected_leaves = Leave.objects.filter(status='Rejected')
  

    context = {
        'get_all_rejected_leaves': get_all_rejected_leaves, 
    }
    return render(request, 'admin_users/leaves/rejected-leaves.html', context)


#End of Leave Function


#ALL SALARY ADVANCE FUNCTIONS


#Pending 
def pending_salary_adv(request):
   
    get_all_pending_salary_adv = SalaryAdvance.objects.filter(approval_status='Pending')
    context = {
        'get_all_pending_salary_adv': get_all_pending_salary_adv, 
    }
    return render(request, 'admin_users/advance/pending-advance.html', context)


def approved_salary_advc(request):
    
    approved_salary_advc = SalaryAdvance.objects.filter(approval_status='Approved')

    context = {
        'approved_salary_advc': approved_salary_advc, 
    }
    return render(request, 'admin_users/advance/approved-advance.html', context)


def rejected_salary_adv(request):
    rejected_salary_advances = SalaryAdvance.objects.filter(approval_status='Rejected')

    context = {
        'rejected_salary_adv': rejected_salary_advances, 
    }
    return render(request, 'admin_users/advance/rejected-advance.html', context)


#End of Salary Advance Function


#Emplyees function

def all_employee(request):
    
    users = User.objects.all()
    
    context = {'users': users}
    return render(request, 'admin_users/employees/all_employees.html', context)

def add_employee(request):
    return render(request, 'admin_users/employees/add-employee.html')