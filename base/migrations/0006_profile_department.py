# Generated by Django 5.1.5 on 2025-01-30 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_remove_profile_address_remove_profile_department_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='department',
            field=models.CharField(blank=True, choices=[('IT', 'IT'), ('HR', 'HR')], max_length=100, null=True),
        ),
    ]
