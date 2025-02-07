from django.urls import path
from .views import (
    add_employee, 
    create_employee, 
    leave_request, 
    salary_advance_request, 
    vett_salary_advc_request, 
    vett_leave_request,
    all_employee,
    pending_leaves,
    approved_leaves,
    rejected_leaves,

    #salary advc
    pending_salary_adv,
    approved_salary_advc,
    rejected_salary_adv,
    all_employee,

)

app_name = "admin_users"

urlpatterns = [
    path('add-employee/', add_employee, name='add_employee'),
    path('create-employee/', create_employee, name='create_employee'),
    path('leave-request/', leave_request, name='leave_request'),
    path('salary-advance-request/', salary_advance_request, name='salary_advance_request'),
    path('vett_salary_advc_request/<int:id>/', vett_salary_advc_request, name='vett_salary_advc_request'),
    path('vett-leave-request/<int:id>/', vett_leave_request, name='vett_leave_request'),
    path('all_employee/', all_employee, name='all_employee'),

    #leave urls
    path('pending_leaves/', pending_leaves, name='pending_leaves'),
    path('approved_leaves/', approved_leaves, name='approved_leaves'),
    path('rejected_leaves/', rejected_leaves, name='rejected_leaves'),


    #salary advance urls
    path('pending_salary_adv/', pending_salary_adv , name='pending_salary_adv'),
    path('approved_salary_advc/', approved_salary_advc, name='approved_salary_advc'),
    path('rejected_salary_adv/', rejected_salary_adv, name='rejected_salary_adv'),


    #Employyes
    path('all_employee/', all_employee, name='all_employee'),
    path('add-employee/', add_employee, name='add_employee'),
]
