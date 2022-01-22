from django.contrib import admin
from .models import Attendance, PermissionAttendance, Lab_Attendance

# Register your models here.
admin.site.register([Attendance, PermissionAttendance, Lab_Attendance])
