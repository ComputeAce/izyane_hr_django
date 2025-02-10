from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from PIL import Image
import random
import os
class Profile(models.Model):
    DEPARTMENT_CHOICES = [
        ('IT', 'IT'),
        ('HR', 'HR'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, null=True, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)
    nhima_number = models.IntegerField(blank=True, null= True) 
    nrc_back = models.ImageField(upload_to='nrc', blank=True, null=True)
    nrc_front = models.ImageField(upload_to='nrc', blank=True, null=True)
    ssn = models.IntegerField(null=True, blank=True)
    tpin = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    """ 
    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)

            img = Image.open(self.image.path)
            try:
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            finally:
                img.close()

            random_number = random.randint(10000000, 99999999)
            base_path, ext = os.path.splitext(self.image.name)
            new_filename = f'{random_number}{ext}'
            new_path = os.path.join('profile_pics', new_filename)
        
            old_full_path = self.image.path
            new_full_path = os.path.join(os.path.dirname(old_full_path), new_filename)
            
            os.rename(old_full_path, new_full_path)
            self.image.name = new_path
            super().save(*args, **kwargs)
        """


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
    status_choices = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')


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
    tenor = models.IntegerField(null=True, blank=True)
    reason = models.TextField()

    def __str__(self):
        return f"Salary Advance for {self.user.username} ({self.amount})"



class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return now() < self.created_at + timedelta(hours=1)