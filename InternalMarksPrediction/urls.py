from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('report_pdf/<int:id>',views.student_report_render_pdf_view, name='student_report_render_pdf_view'),

]