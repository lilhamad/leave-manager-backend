from django.contrib import admin
from .models import Leave
from django.contrib.auth.admin import UserAdmin
from django.db import models


class LeaveAdmin(admin.ModelAdmin):
    model = Leave
    list_display = ['start_date', 'employee', 'application_date', 'status']

admin.site.register(Leave, LeaveAdmin)
