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
    path('', views.assignment_home, name = 'assignment_home'),
    path('batch/<int:id>', views.assignment_batch, name='assignment_batch_view'),
    path('session/<int:id>', views.assignment_session_view, name = 'assignment_session_view'),
    path('create_assignment/<int:id>', views.create_assignment, name = 'create_assignment'),
    path('check_assignment/<int:id>', views.assignment_check_view, name='assignment_check_view'),
    path('assignment_done/<int:id>/<int:ids><int:num>', views.assignment_done, name = 'assignment_done'),
    path('assignment_edit/<int:id>/', views.assignment_edit, name = 'assignment_edit'),
    path('assignment_deletet/<int:id>/', views.assignment_delete, name = 'assignment_delete'),


    path('labhome/', views.lab_assignment_home, name = 'lab_assignment_home'),
    path('lab_batch/<int:id>', views.lab_assignment_batch, name='lab_assignment_batch_view'),

    path('lab_group/<int:id>', views.lab_assignment_group, name='lab_assignment_group_view'),

    path('labsession/<int:id>/<int:sid>', views.lab_assignment_session_view, name = 'lab_assignment_session_view'),
    path('create_lab_assignment/<int:gid>/<int:id>', views.create_lab_assignment, name = 'create_lab_assignment'),
    path('check_labassignment/<int:id>/<int:gid>', views.lab_assignment_check_view, name='lab_assignment_check_view'),
    path('labassignment_done/<int:id>/<int:ids><int:num>', views.lab_assignment_done, name = 'lab_assignment_done'),
    path('labassignment_edit/<int:id>/', views.lab_assignment_edit, name = 'lab_assignment_edit'),
    path('lab_assignment_deletet/<int:id>/', views.lab_assignment_delete, name = 'lab_assignment_delete'),

]