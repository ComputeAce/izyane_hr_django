from django.urls import path
from .views import (
    leave_request,
    employee_dashboard,
    salary_advc_form,
    leave_form,
    submit_form_salary_advc,
    agreement_view,
)

app_name = "employees"

urlpatterns = [
    path('dashboard/', employee_dashboard, name='employee_dashboard'),
    path('submit-salary-advance/', submit_form_salary_advc, name='submit_form_salary_advc'),
    path('leave/request/', leave_request, name='leave_request'),
    path('salary-advance/form/', salary_advc_form, name='salary_advc_form'),
    path('leave/form/', leave_form, name='leave_form'),
    path('agreement/', agreement_view, name='agreement_view')
]
