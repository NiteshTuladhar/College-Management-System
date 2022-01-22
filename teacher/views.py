from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .forms import Edit_Teacher_Form
from Accounts.models import Account
from .models import Teacher
from student.models import Course, Batch, Student, Session
from Accounts.decorators import unauthenticated_user, authenticated_user
from student.models import Student, Faculty, Batch, Session, Course
from notices.models import NoticeBoard
# Create your views here.
@authenticated_user
def edit_teacher_form(request):
    account = Account.objects.latest('id')
    form = Edit_Teacher_Form()
    if request.method == "POST":
        form = Edit_Teacher_Form(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = account
            print(form.user)
            form.save()
            messages.success(request,"Teacher Has been added.")
            return redirect('dashboard')

    context={
        'current' : 'current',
        'form': form
    }

    return render(request, 'add_form/teacher_edit_form.html', context)
    
@authenticated_user
def teacher_home_page(request):
    teacher_id = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.filter(teacher_id_id=teacher_id)
    n = []
    for c in course:
       n.append(c.session_id)

    account_info = Account.objects.get(id=request.user.id)
    notice = NoticeBoard.objects.filter(semester__in = n)
    print(notice)
   

    context = {
        'homecurrent' : 'current',
        'course': course,
        'teacher_id' : teacher_id,
        'account_info' : account_info,
        'notice': notice,
    }


    return render(request,'homepage/teacher_homepage.html', context)


def teacher_faculty_view(request):
    account_info = Account.objects.get(id=request.user.id)
    faculty = Faculty.objects.all()
    context = {

        'teachercurrent' : 'current',
        'faculty': faculty,
        'account_info' : account_info
            }

    return render(request,'teacher_view/faculty_view.html', context)


def teacher_batch_view(request, id):
    account_info = Account.objects.get(id=request.user.id)
    faculty_detail = Faculty.objects.get(id=id)
    batch = Batch.objects.filter(faculty_id=faculty_detail.id)

    context = {
        'teachercurrent' : 'current',
        'faculty_id': faculty_detail,
        'batch': batch,
        'account_info' : account_info,
    }

    return render(request, 'teacher_view/batch_view.html', context)

def teacher_student_view(request, id):
    account_info = Account.objects.get(id=request.user.id)
    student = Student.objects.filter(batch_id=id)

    context = {
        'teachercurrent' : 'current',
        'student': student,
        'account_info' : account_info,
    }

    return render(request,'teacher_view/student_view.html', context)