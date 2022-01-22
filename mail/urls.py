from django.urls import path
from . import views

urlpatterns = [

    path('contactus', views.contactus, name='contactus'),
    path('contactus/view', views.viewmail, name='view_contactus'),
    path('contactus/student_msg', views.viewmailStudent, name='student_msg_view'),
    path('contactus/reply/<int:id>', views.replyMail, name='replyMail'),
    path('contactus/reply_process/<int:id>', views.saveReply, name='saveReply'),

]