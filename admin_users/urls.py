from django.urls import path
from .views import (
    user_management, 
    add_employee, 
    create_employee, 
    leave_request, 
    salary_advance_request, 
    vett_salary_advc_request, 
    vett_leave_request
)

app_name = "admin_users"

urlpatterns = [
    path('user-management/', user_management, name='user_management'),
    path('add-employee/', add_employee, name='add_employee'),
    path('create-employee/', create_employee, name='create_employee'),
    path('leave-request/', leave_request, name='leave_request'),
    path('salary-advance-request/', salary_advance_request, name='salary_advance_request'),
    path('vett-salary-request/<int:id>/', vett_salary_advc_request, name='vett_salary_request'),
    path('vett-leave-request/<int:id>/', vett_leave_request, name='vett_leave_request'),
]
