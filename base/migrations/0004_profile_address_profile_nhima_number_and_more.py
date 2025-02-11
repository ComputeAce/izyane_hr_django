# Generated by Django 5.1.5 on 2025-02-05 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_leave_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='nhima_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='nrc_back',
            field=models.ImageField(blank=True, null=True, upload_to='nrc'),
        ),
        migrations.AddField(
            model_name='profile',
            name='nrc_front',
            field=models.ImageField(blank=True, null=True, upload_to='nrc'),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='ssn',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='tpin',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
