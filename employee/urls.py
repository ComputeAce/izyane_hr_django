from django.urls import path
from .views import (
    leave_request,
    employee_dashboard,
    salary_advc_form,
    leave_form,
    salary_advc_request,
)

app_name = "employees"

urlpatterns = [
    path('dashboard/', employee_dashboard, name='employee_dashboard'),
    path('salary-advance/request/', salary_advc_request, name='salary_advc_request'),
    path('leave/request/', leave_request, name='leave_request'),
    path('salary-advance/form/', salary_advc_form, name='salary_advc_form'),
    path('leave/form/', leave_form, name='leave_form'),
]
