from django.urls import path

from .import views

urlpatterns = [

    path('', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.create_event, name='event_new'),
    path('event/<int:event_id>/details/', views.event_details, name='event-detail'),
    path('event/edit/<int:id>/', views.EventEdit, name='event_edit'),
    path('add_eventmember/<int:event_id>', views.add_eventmember, name='add_eventmember'),
    path('event/<int:pk>/remove', views.EventMemberDeleteView.as_view(), name="remove_event"),

    path('teacher/', views.TeacherCalendarView.as_view(), name='teacher_calendar'),
    path('student/', views.StudentCalendarView.as_view(), name='student_calendar'),
]