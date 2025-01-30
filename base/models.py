from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    DEPARTMENT_CHOICES = [
        ('IT', 'IT'),
        ('HR', 'HR'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    


class Employee(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    ]

    EMPLOYMENT_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    POSITION_TYPE_CHOICES = [
        ('Junior', 'Junior'),
        ('Senior Develope', 'Senior'),
        ('Lead', 'Lead'),
        ('Manager', 'Manager'),
        ('Director', 'Director'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES, default='Full Time')
    position = models.CharField(max_length=100)
    employment_status = models.CharField(max_length=50, choices=EMPLOYMENT_STATUS_CHOICES, default='Active')
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return f'{self.user.username} Employee'
    

class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Vacation', 'Vacation'),
        ('Leave', 'Leave'),
        ('Bereavement', 'Bereavement'),
        ('Paternity', 'Paternity'),
        ('Maternity', 'Maternity'),
        ('Time Off with Pay', 'Time Off with Pay'),
        ('Others', 'Others'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES, default='Others')
    hr_approved = models.BooleanField(default=False)
    director_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Leave'
 
class SalaryAdvance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_date = models.DateField(auto_now_add=True)
    approval_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    repayment_start_date = models.DateField(null=True, blank=True)
    repayment_end_date = models.DateField(null=True, blank=True)
    repayment_months = models.IntegerField(null=True, blank=True)
    reason = models.TextField()

    def __str__(self):
        return f"Salary Advance for {self.user.username} ({self.amount})"

