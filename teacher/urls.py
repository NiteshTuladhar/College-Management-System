from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('editform', views.edit_teacher_form, name = 'teacher_edit_form'),
    path('teacher/dashboard', views.teacher_home_page, name = "teacher_homepage"),
    path('teacher/faculty_view', views.teacher_faculty_view, name = 'teacher_faculty_view'),
    path('teacher/batch_view/<int:id>', views.teacher_batch_view, name = 'teacher_batch_view'),
    path('teacher/student_view/<int:id>', views.teacher_student_view, name = 'teacher_student_view'),

]