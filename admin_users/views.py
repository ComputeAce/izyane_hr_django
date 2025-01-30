from django.shortcuts import render

def user_management(request):
    return render(request, 'admin_users/user_management.html')


def add_employee(request):
    return render(request, 'admin_users/add-employee.html')
