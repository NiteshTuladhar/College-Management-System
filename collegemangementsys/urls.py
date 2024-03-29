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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage,name='homepage'),
    path('Accounts/', include('Accounts.urls')),
    path('EditForm/', include('student.urls')),
    path('Teacher/', include('teacher.urls')),
    path('Staff/', include('staff.urls')),
    path('Attendance/', include('attendance.urls')),
    path('Assignment/', include('assignments.urls')),
    path('Assesment/', include('assessment.urls')),
    path('Calendar/', include('collegecalendar.urls')),
    path('notice/', include('notices.urls')),
    path('mail/', include('mail.urls')),
    path('payments/', include('payments.urls')),
    path('marks/', include('InternalMarksPrediction.urls')),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form/passwordresetview.html'
    ), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_form/passwordResetDoneView.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_form/passwordResetConfirmView.html'
    ), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_form/PasswordResetCompleteView.html'
    ), name='password_reset_complete'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)