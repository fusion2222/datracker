from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from datracker.models import Employee

@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    model = Employee
