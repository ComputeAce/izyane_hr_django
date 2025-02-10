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


def agreement_view(request):

    salary_advance_data = request.session.get("salaryAdvance", {})
    amount = float(salary_advance_data.get("total", 0))  
    tenor = int(salary_advance_data.get("tenor", 1)) 
    reason = salary_advance_data.get("reason", "No reason provided")


    if tenor != 0:
        monthly_deduction = amount / tenor
    else:
        monthly_deduction = 0

    context = {
        'amount': amount,
        'tenor': tenor,
        'reason': reason,
        'monthly_deduction': monthly_deduction
    }
    if request.method == "POST":

        request.session['salaryAdvance'] = {
            'total': amount,
            'tenor': tenor,
            'reason': reason
        }
        user = request.user
        create_record = SalaryAdvance.objects.create(user = user, amount = amount, tenor = tenor, reason = reason)
        create_record.save()

        get_salary_adv_of_user = SalaryAdvance.objects.get(user = request.user, approval_status = 'Pending')

        salary_advc_obj = NewSalaryAdvcNotification(get_salary_adv_of_user.id)
        salary_advc_obj.send_mail_to_applicant()
        salary_advc_obj.send_mail_to_manager()
        messages.info(request, 'Salary advance application submitted successfully.')
        return redirect('employees:submit_form_salary_advc')

    
    return render(request, 'employee/agreement.html', context)

#zawadi15
def submit_form_salary_advc(request):
    get_user_salary_advc = SalaryAdvance.objects.filter(user=request.user)

    if request.method == "POST":
        total = request.POST.get("total")
        tenor = request.POST.get("tenor")
        reason = request.POST.get("reason")

        user = request.user

        try:
            check_pending_requests = SalaryAdvance.objects.filter(user=user, approval_status='Pending')
            if check_pending_requests.exists():
                messages.info(request, "You already have a pending application. Please wait for it to be processed.")
                return redirect('employees:submit_form_salary_advc')
            
            request.session["salaryAdvance"] = {
                "total": total,
                "tenor": tenor,
                "reason": reason,
            }
            print("Saved session data:", request.session["salaryAdvance"])
            return redirect('employees:agreement_view')  

        except Exception as e:
    
            print(f"Error processing salary advance request: {e}")
            messages.warning(request, "Invalid request, please try again.")
            return redirect('employees:submit_form_salary_advc')
            

    context = {
        'get_user_salary_advc': get_user_salary_advc
    }

    return render(request, 'employee/salary_advc.html', context)
