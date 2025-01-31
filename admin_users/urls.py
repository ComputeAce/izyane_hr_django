from django.urls import path
from .views import  user_management, add_employee, create_employee, leave_request, salary_advance_request

app_name = "admin_users"
urlpatterns = [
    path('user_management', user_management, name='user_management'),
    path('add_employee', add_employee, name='add_employee'),
    path('create_employee', create_employee, name='create_employee'),
    path('leave_request/', leave_request, name='leave_request'),
    path('salary_advance_request/', salary_advance_request, name='salary_advance_request')
]
