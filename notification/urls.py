from django.urls import path
from .views import (
    send_mail_new_employee
)

urlpatterns = [
    path('send_new_employee', send_mail_new_employee , name='send_new_employee')
]
