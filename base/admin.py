from django.contrib import admin
from .models import Employee, LeaveRequest, SalaryAdvance

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'hire_date', 'department', 'is_admin', 'phone_number', 'address')
    search_fields = ('user__username', 'department', 'phone_number')
    list_filter = ('department', 'is_admin')

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'status')
    search_fields = ('employee__user__username', 'status')
    list_filter = ('status', 'start_date', 'end_date')

@admin.register(SalaryAdvance)
class SalaryAdvanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'amount', 'request_date', 'status')
    search_fields = ('employee__user__username', 'status')
    list_filter = ('status', 'request_date')
