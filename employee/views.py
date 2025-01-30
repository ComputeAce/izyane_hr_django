from django.shortcuts import render
from base.models import Leave, SalaryAdvance
from django.contrib import messages
from datetime import timedelta, datetime

def leave_request(request):
    return render(request, 'base/leave_request.html')


def employee_dashboard(request):
    return render(request, 'employee/dashboard.html')



def leave_form(request):
    user = request.user
    get_user_leaves = Leave.objects.filter(user=user)
    context = {
        'get_user_leaves': get_user_leaves
    }
    return render(request, 'employee/apply_leave.html', context)

def salary_advc_form(request):
    user = request.user
    get_user_salary_advc = SalaryAdvance.objects.filter(user=user)
    print(get_user_salary_advc)
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

        leave = Leave(user=request.user, start_date=start_date, end_date=end_date, reason=reason, leave_type=leave_type)
        leave.save()

    messages.info(request, 'Leave request submitted successfully.')
    return render(request, 'employee/apply_leave.html')


def salary_advc_request(request):
    if request.method == 'POST':
        user = request.user
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        repayment_start_date = request.POST.get('repayment_start_date')
        repayment_months = request.POST.get('repayment_months')
        
    
        repayment_start_date = repayment_start_date and datetime.strptime(repayment_start_date, '%Y-%m-%d').date()
        salary_advance = SalaryAdvance(
            user=user,
            amount=amount,
            reason=reason,
            repayment_start_date=repayment_start_date,
            repayment_months=repayment_months
        )
        salary_advance.save()

        messages.success(request, "Salary Advance Request submitted successfully.")
    return render(request, 'employee/salary_advc.html')
