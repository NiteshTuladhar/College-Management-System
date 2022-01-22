from django.urls import path
from . import views


urlpatterns = [

    path('editform', views.edit_form_staff, name = 'staff_edit_form'),

]