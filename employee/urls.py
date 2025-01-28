from django.urls import path
from .views import leave_request

app_name = "employees"
urlpatterns = [
    path('leave_request/', leave_request, name='leave_request')
]
