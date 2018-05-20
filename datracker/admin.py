from djsingleton.admin import SingletonAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from datracker.models import Employee, SiteSettings


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    model = Employee

@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    model = SiteSettings
