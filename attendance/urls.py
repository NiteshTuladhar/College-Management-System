"""collegemangementsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path
from . import views

urlpatterns = [

    path('attendance_view', views.attendance_homepage, name = 'attendance_homepage'),
    path('faculty_view/<int:id>', views.attendance_faculty_detail, name='attendance_faculty_detail'),
    path('attendance/faculty/', views.attendance_faculty_view, name='attendance_faculty_view'),
    path('attendance/batch/<int:id>', views.attendance_batch_view, name="attendance_course_view"),
    path('attendance/session/<int:id>', views.attendance_session_view, name='attendance_session_view'),
    path('attendace/presnt/<int:id>', views.attendance_present, name='attendance_preseent'),
    path('attendace/absent/<int:id>', views.attendance_absent, name='attendance_absent'),


    path('lab_attendance_view', views.lab_attendance_homepage, name = 'lab_attendance_homepage'),
    path('lab_faculty_view/<int:id>', views.lab_attendance_faculty_detail, name='lab_attendance_faculty_detail'),
    
    path('lab_attendance/faculty/', views.lab_attendance_faculty_view, name='lab_attendance_faculty_view'),
    path('lab_attendance/batch/<int:id>', views.lab_attendance_batch_view, name="lab_attendance_course_view"),
    path('lab_attendance/session/<int:id>/<int:sid>', views.lab_attendance_session_view, name='lab_attendance_session_view'),
    path('lab_attendace/presnt/<int:id>', views.lab_attendance_present, name='lab_attendance_preseent'),
    path('lab_attendace/absent/<int:id>', views.lab_attendance_absent, name='lab_attendance_absent'),

    path('lab_attendance/group/<int:id>', views.lab_attendance_group_view, name='lab_attendance_group_view'),
]