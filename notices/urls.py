from django.urls import path

from .import views

urlpatterns = [
    path('add_notice/', views.add_admin_noticeboard, name='admin_add_notice'),
    path('add_announcement/', views.add_admin_announcement, name='admin_add_announcement'),
    path('teacher/add_notice/', views.add_teacher_noticeboard, name='add_teacher_noticeboard'),
    path('teacher/add_announcement/', views.add_teacher_announcement, name='add_teacher_announcement'),

]