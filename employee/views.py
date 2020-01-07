from django.shortcuts import render

# Create your views here.
from .models import Employee
from django.contrib.auth.admin import UserAdmin
from django.db import models


class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    # list_display = ['first_name', 'last_name']

admin.site.register(Employee, EmployeeAdmin)