# Generated by Django 5.1.5 on 2025-01-30 07:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_profile_delete_employeeprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='department',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='hire_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='position',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profile_picture',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='salary',
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
