# cal/views.py

from datetime import datetime, date
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta
import calendar
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import *
from .utils import Calendar, TCalendar, SCalendar
from .forms import EventForm, AddMemberForm
from notices.models import NoticeBoard


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarView(LoginRequiredMixin, generic.ListView):

    model = Event
    template_name = 'calendar/calendar.html'

    def get_context_data(self, **kwargs):

        account_info = Account.objects.get(id=self.request.user.id) 
        notices_count = NoticeBoard.objects.all().order_by('-notice_date').count() 
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        print(html_cal)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['account_info'] = account_info
        context['calendarcurrent'] = 'current'
        context['notice_count'] = notices_count

        return context


@login_required
def create_event(request):  
    
    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()  
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        messages.success(request,"Event Has Been Created.")
        return HttpResponseRedirect(reverse('calendar'))

    return render(request, 'calendar/event.html', {'form': form,'account_info':account_info,'calendarcurrent' : 'current','notice_count' : notices_count,})



@login_required
def event_details(request, event_id):
    account_info = Account.objects.get(id=request.user.id) 
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count() 
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {
        'calendarcurrent' : 'current',
        'event': event,
        'eventmember': eventmember,
        'account_info' : account_info,
        'notice_count' : notices_count,
    }
    return render(request, 'calendar/event-details.html', context)



def EventEdit(request, id):

    
    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    event = Event.objects.get(id=id)

    form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        messages.success(request,"Event Has Been Updated Successfully")
        
        return redirect('event-detail', event_id=id)

    context = {
        'calendarcurrent':'current',
        'form' : form,
        'account_info' : account_info,
        'notice_count' : notices_count,
    }

    return render(request,'calendar/event_edit.html', context)


def add_eventmember(request, event_id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()  
    forms = AddMemberForm()
    if request.method == 'POST':
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                session = forms.cleaned_data['session']
                EventMember.objects.create(
                    event=event,
                    session=session
                )
                messages.success(request,"Event Members have been added.")
                return redirect('event-detail', event.id)
            else:
                print('--------------User limit exceed!-----------------')
    context = {
        'calendarcurrent' : 'current',
        'form': forms,
        'account_info' : account_info,
        'notice_count' : notices_count,
    }
    return render(request, 'calendar/add_member.html', context)



class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = 'calendar/event_delete.html'
    success_url = reverse_lazy('calendar')





#TEACHER CALENDER VIEW #


class TeacherCalendarView(LoginRequiredMixin, generic.ListView):

    model = EventMember
    template_name = 'calendar/teacher_calendar/teacher_calendar.html'


    def get_context_data(self, **kwargs):

        account_info = Account.objects.get(id=self.request.user.id)
        notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()  
        context = super().get_context_data(**kwargs)
        print('TEACHERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR')
        user = self.request.user

        d = get_date(self.request.GET.get('month', None))
        cal = TCalendar(d.year, d.month, user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['account_info'] = account_info
        context['calendarcurrent'] = 'current'

        context['notice_count'] = notices_count,
        
        return context


class StudentCalendarView(LoginRequiredMixin, generic.ListView):

    model = EventMember
    template_name = 'calendar/teacher_calendar/student_calendar.html'


    def get_context_data(self, **kwargs):

        account_info = Account.objects.get(id=self.request.user.id)
        notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()  
        context = super().get_context_data(**kwargs)
        print('STUDENTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
        user = self.request.user

        d = get_date(self.request.GET.get('month', None))
        cal = SCalendar(d.year, d.month, user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['account_info'] = account_info
        context['calendarcurrent'] = 'current'

        context['notice_count'] = notices_count,

        
        return context