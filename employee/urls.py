from django.urls import path
from .views import leave_request, employee_dashboard, salary_advc_form, leave_form, salary_advc_request

app_name = "employees"
urlpatterns = [
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard'),
    path('salary_advc_request/', salary_advc_request, name='salary_advc_request'),
    path('leave_request/', leave_request, name='leave_request'),
    path('salary_advc_form/', salary_advc_form, name='salary_advc_form'),
    path('leave_form/', leave_form, name='leave_form'),
]
