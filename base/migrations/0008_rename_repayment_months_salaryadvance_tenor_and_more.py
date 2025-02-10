# Generated by Django 5.1.5 on 2025-02-08 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_rename_passwordresttoken_passwordresettoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salaryadvance',
            old_name='repayment_months',
            new_name='tenor',
        ),
        migrations.RemoveField(
            model_name='salaryadvance',
            name='repayment_end_date',
        ),
        migrations.RemoveField(
            model_name='salaryadvance',
            name='repayment_start_date',
        ),
    ]
