# Generated by Django 5.1.5 on 2025-01-29 15:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0002_remove_employee_user_remove_salaryadvance_employee_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('hire_date', models.DateField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('department', models.CharField(blank=True, choices=[('Developer', 'Developer'), ('Operations', 'Operations'), ('Human Resources', 'Human Resources')], max_length=50, null=True)),
                ('employee_type', models.CharField(blank=True, choices=[('Permanent', 'Permanent'), ('Internship', 'Internship'), ('Contract', 'Contract')], max_length=20, null=True)),
                ('position', models.CharField(blank=True, choices=[('Manager', 'Manager'), ('Developer', 'Developer'), ('HR', 'HR'), ('Sales', 'Sales'), ('Admin', 'Admin')], max_length=50, null=True)),
                ('salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('salary_currency', models.CharField(choices=[('KW', 'Kwacha'), ('USD', 'USD'), ('EUR', 'Euro'), ('GBP', 'GBP'), ('INR', 'INR')], default='KW', max_length=3)),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
