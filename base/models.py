from django.db import models
from django.conf import settings

class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('Developer', 'Developer'),
        ('Operations', 'Operations'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hire_date = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"{self.employee.user.username} - {self.status}"

class SalaryAdvance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"{self.employee.user.username} - {self.amount} - {self.status}"