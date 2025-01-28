from django.urls import path
from .views import  user_management, add_employee

app_name = "admin_users"
urlpatterns = [
    path('user_management', user_management, name='user_management'),
    path('add_employee', add_employee, name='add_employee')
]
