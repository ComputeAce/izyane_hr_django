# Generated by Django 5.1.5 on 2025-01-30 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_salaryadvance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaryadvance',
            name='repayment_amount',
        ),
        migrations.AddField(
            model_name='salaryadvance',
            name='repayment_months',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
