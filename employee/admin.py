from django.contrib import admin
from .models import Employee
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.contrib.auth import get_user_model


class EmployeeAdmin(admin.ModelAdmin):
    model = get_user_model()
    list_display = ['email', 'first_name', 'last_name', 'is_admin', 'is_staff']

admin.site.register(get_user_model(), EmployeeAdmin)
