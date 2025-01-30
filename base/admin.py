from django.contrib import admin
from .models import Profile, Leave, SalaryAdvance

admin.site.register(Profile)
admin.site.register(Leave)
admin.site.register(SalaryAdvance)