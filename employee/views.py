from django.shortcuts import render, redirect
from base.models import Leave, SalaryAdvance
from django.contrib import messages
from datetime import timedelta, datetime
from notification.views import (
    NewLeaveNotification,
    NewSalaryAdvcNotification
)


def leave_request(request):
    return render(request, 'base/leave_request.html')


def employee_dashboard(request):
    return render(request, 'employee/dashboard.html')


def leave_form(request):
    user = request.user.username

    get_user_leaves = Leave.objects.filter(user__username=user)
    context = {
        'get_user_leaves': get_user_leaves
    }   
    return render(request, 'employee/apply_leave.html', context)

def salary_advc_form(request):
    user = request.user.username
    get_user_salary_advc = SalaryAdvance.objects.filter(user__username=user)
    for adv in get_user_salary_advc:
        print(adv)
    context = { 

        'get_user_salary_advc': get_user_salary_advc
    }
    return render(request, 'employee/salary_advc.html', context)


def leave_request(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        leave_type = request.POST.get('leave_type')

        existing_leave = Leave.objects.filter(user=request.user, status='Pending').first()

        if existing_leave:
            messages.warning(request, 'You already have a pending leave request. Please wait for it to be processed before submitting a new request.')
            return redirect('employees:leave_form')
        

        else:

            leave = Leave(user=request.user, start_date=start_date, end_date=end_date, reason=reason, leave_type=leave_type)
            leave.save()

            get_leave_obj = Leave.objects.get(user = request.user, status = 'Pending')

            create_leave_obj = NewLeaveNotification(get_leave_obj.id)
            create_leave_obj.send_mail_to_applicant()
            create_leave_obj.send_mail_to_manager()

            messages.info(request, 'Leave request submitted successfully.')
            return redirect('employees:leave_form')



def salary_advc_request(request):
    if request.method == 'POST':
        user = request.user
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        repayment_start_date = request.POST.get('repayment_start_date')
        repayment_months = request.POST.get('repayment_months')
        
    
        repayment_start_date = repayment_start_date and datetime.strptime(repayment_start_date, '%Y-%m-%d').date()
        check_obj_exists = SalaryAdvance.objects.filter(user = request.user, approval_status = 'Pending')
        if check_obj_exists.exists():
            messages.warning(request, 'You already have a pending leave request. Please wait for it to be processed before submitting a new request.' )
            return redirect('employees:salary_advc_form')
        
        else:
            salary_advance = SalaryAdvance(
                user=user,
                amount=amount,
                reason=reason,
                repayment_start_date=repayment_start_date,
                repayment_months=repayment_months
            )
            salary_advance.save()
            user = request.user
            get_salary_obj = SalaryAdvance.objects.get(user = user, approval_status = 'Pending')
            advc_id = get_salary_obj.id

            advance_obj = NewSalaryAdvcNotification(advc_id)
            advance_obj.send_mail_to_applicant()
            advance_obj.send_mail_to_manager()
            messages.success(request, "Salary Advance Request submitted successfully...")
            return redirect('employees:salary_advc_form')
