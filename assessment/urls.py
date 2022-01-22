from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.assesment_home, name='assesment_home'),
    path('batch/<int:id>', views.assessment_batch, name='assessment_batch'),
    path('session/<int:id>', views.assessment_session_view, name = 'assessment_session_view'),
    path('create_assessment/<int:id>', views.create_assessment, name='create_assessment'),
    path('assessment_check_view/<int:id>', views.assessment_check_view, name='assessment_check_view'),
    path('getmarks/<int:id>/<int:sid>', views.getmarks, name='getmarks'),
    path('assessment_edit/<int:id>/', views.assessment_edit, name = 'assessment_edit'),

    path('assesment_delete/<int:id>/', views.assesment_delete, name = 'assesment_delete'),

    path('error/', views.errorpage, name = 'errorpage'),


    path('assesment_delete/<int:id>/', views.assesment_delete, name = 'assesment_delete'),
    path('error/', views.errorpage, name = 'errorpage'),


]