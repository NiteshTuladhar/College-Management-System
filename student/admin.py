from django.contrib import admin
from .models import Student, Session, Course, Batch, Faculty, Group,CourseColor
# Register your models here.

admin.site.register([Student, Session, Course, Batch, Faculty,Group,CourseColor])
