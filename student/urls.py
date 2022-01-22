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
from . import views

urlpatterns = [

	path('student/', views.edit_student_form, name='editform_student'),
	path('faculty/', views.edit_faculty_form, name='edit_faculty_form'),
	path('faculty_view/', views.faculty_view, name = 'faculty_view'),
	path('faculty_detail/<int:id>', views.faculty_detail, name='faculty_detail'),
    path('session_view/<int:id>', views.session_view, name = 'session_view'),
    path('course_view/<int:id>', views.course_view, name = 'course_view'),
	path('batch_add/<int:id>', views.edit_batch_form, name='add_batch_form'),
	path('student_view/<int:id>', views.student_view, name='student_view'),
    path('add_session/<int:id>', views.add_session, name='edit_session_form'),
    path('add_course/<int:id>', views.add_course, name='edit_course_form'),
    

    path('faculty_edit/<int:id>',views.edit_individual_faculty, name='edit_individual_faculty'),
    path('faculty_delete/<int:id>', views.delete_faculty, name="delete_faculty"),

    path('group/', views.edit_group_form, name='edit_group_form'),
    path('group_edit/<int:id>',views.edit_individual_group, name='edit_individual_group'),
    path('group_delete/<int:id>', views.delete_group, name="delete_group"),

    path('batch_edit/<int:id>',views.edit_individual_batch, name='edit_individual_batch'),
    path('batch_delete/<int:id>', views.delete_batch, name="delete_batch"),

    path('session_edit/<int:id>',views.edit_session, name='edit_session'),
    path('session_delete/<int:id>', views.delete_session, name="delete_session"),

    path('course_edit/<int:id>', views.edit_course, name='edit_course'),
    path('course_delete/<int:id>', views.delete_course, name="delete_course"),

    path('student_edit/<int:id>',views.edit_student, name='edit_student'),
    path('studenty_delete/<int:id>', views.remove_student, name="remove_student"),

    path('faculty_student_view/', views.faculty_student_view, name = 'faculty_student_view'),
    path('batch_student_view/<int:id>', views.faculty_batch_view, name='faculty_batch_view'),

    path('teacher_view/', views.teacher_view, name = 'teacher_view'),
    path('teacher_edit/<int:id>',views.edit_teacher, name='edit_teacher'),
    path('teacher_delete/<int:id>', views.remove_teacher, name="remove_teacher"),
    # Student Profile Url Starts Here

    path('student/profile', views.student_homepage, name="student_homepage"),
    path('student/report', views.studentReport, name='studentreport'),

    
    path('student/notice_board', views.student_notice_board, name='student_notice_board'),
    
    path('student/assignment/', views.student_assignment, name='student_assignment'),
    path('student/assignment_details/<int:id>',views.student_assignment_details, name='student_assignment_details'),
    path('submit_assignment/<int:id>',views.submit_assignment,name='submit_assignment'),


    path('student/lab_assignment/', views.student_lab_assignment, name='student_lab_assignment'),
    path('student/lab_assignment_details/<int:id>',views.student_lab_assignment_details, name='student_lab_assignment_details'),
    path('submit_lab_assignment/<int:id>',views.submit_lab_assignment,name='submit_lab_assignment'),
    

    path('student/dashboard', views.student_dashboard, name='student_dashboard'),


    path('edit_session_status/', views.edit_session_status, name='edit_session_status'),
    path('change_session_status/<int:id>', views.change_session_status, name='change_session_status'),
    path('student/student_dashboard/<int:id>', views.student_course_detail, name='student_course_detail'),
    path('student/student_profile', views.student_profile, name='student_profile'),

]