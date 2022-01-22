from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NoticeBoard
from .forms import FormNoticeBoard
from teacher.models import Teacher
from student.models import Course
# Create your views here.

def add_admin_noticeboard(request):
    account_info = request.user
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    form = FormNoticeBoard()
    if request.method == "POST":
        form = FormNoticeBoard(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.notice_annoucer = account_info
            form.type = 'Notice'
            form.save()
            messages.success(request,"Notice Added To The Admin Board.")
            return redirect('homepage')
        

    context= {
        'form': form,
        'homecurrent': 'current',
        'account_info' : account_info,
        'notice_count' : notices_count,
    }

    return render(request,'notice/admin_add_notice.html', context)


def add_admin_announcement(request):
    account_info = request.user
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    form = FormNoticeBoard()
    if request.method == "POST":
        form = FormNoticeBoard(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.notice_annoucer = account_info
            form.type = 'Announcement'
            form.save()
            messages.success(request,"Announcement Added To The Admin Board.")
            return redirect('homepage')
        

    context= {
        'form': form,
        'homecurrent':'current',
        'account_info' : account_info,
        'notice_count' : notices_count,
    }

    return render(request,'notice/admin_add_announcement.html', context)


def add_teacher_noticeboard(request, *args, **kwargs):
    account_info = request.user
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.filter(teacher_id=teacher)
    print(course)
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        semester = request.POST.get('semester')
        for c in course:
            print(str(c.session_id))
            print(semester)
            if str(c.session_id) == semester:
                semester = c.session_id
        print(type(semester))
     
        try:
            notice = NoticeBoard.objects.create(notice_annoucer=account_info, notice_title=title, notice_description=description, semester=semester, type='Notice')
            messages.success(request,"Notice is successfully sent to all related faculty.")
        except:
            messages.error(request,"Sorry for Inconvinience!!! Some Error Occured")

        return redirect('teacher_homepage')


    context= {
        
        'homecurrent': 'current',
        'account_info' : account_info,
        'notice_count' : notices_count,
        'course': course,
    }

    return render(request,'notice/add_teacher_noticeboard.html', context)


def add_teacher_announcement(request):
    account_info = request.user
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    teacher = Teacher.objects.get(user_id=request.user.id)

    course = Course.objects.filter(teacher_id=teacher)
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        semester = request.POST.get('semester')
        for c in course:
            print(str(c.session_id))
            print(semester)
            if str(c.session_id) == semester:
                semester = c.session_id
        print(type(semester))
     
        try:
            notice = NoticeBoard.objects.create(notice_annoucer=account_info, notice_title=title, notice_description=description, semester=semester, type='Announcement')
            messages.success(request,"Announcement is successfully sent to all related faculty.")
        except:
            messages.error(request,"Sorry for Inconvinience!!! Some Error Occured")

        return redirect('teacher_homepage')
    context= {
     
        'homecurrent':'current',
        'account_info' : account_info,
        'notice_count' : notices_count,
        'course' : course,
    }

    return render(request,'notice/add_teacher_announcement.html', context)