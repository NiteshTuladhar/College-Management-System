from django.shortcuts import render, redirect, HttpResponseRedirect
import datetime
from .models import *
from student.models import Session, Student, Course, Batch, Faculty
import datetime
# Create your views here.
def attendance_homepage(request,id):

    account_info = Account.objects.get(id=request.user.id)
    current_time = datetime.datetime.now()
    course = Course.objects.filter(session_id = id)
    session = Session.objects.filter(id = course.id)

    context = {
        'current' : 'current',
        'current_time': current_time,
        'account_info' : account_info,
    }
    return render(request, 'attendance/attendance_homepage.html', context)


def attendance_faculty_detail(request, id):

    account_info = Account.objects.get(id=request.user.id)
    faculty_detail = Faculty.objects.get(id=id)
    batch = Batch.objects.all()

    context = {
        'current' : 'current',
        'faculty_id': faculty_detail,
        'batch': batch,
        'account_info' : account_info,
    }

    return render(request,'attendance/attendance_faculty.html', context)



def attendance_faculty_view(request):

    account_info = Account.objects.get(id=request.user.id)
    teacher = Teacher.objects.get(user_id = request.user.id)
    faculty = Faculty.objects.all()


    context = {

        'faculty' : faculty,
        'account_info' : account_info,
        'current' : 'current',

    }

    return render(request,'attendance/attendance_faculty_view.html', context)


def attendance_batch_view(request, id):

    account_info = Account.objects.get(id=request.user.id)
    
    faculty = Faculty.objects.get(id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.filter(faculty_id=id,teacher_id_id=teacher)
    course_length = len(course)
    if course_length == 0:
        return redirect('errorpage')
    context = {
        'current' : 'current',
        'course': course,
        'teacher': teacher,
        'account_info' : account_info,
    }

    return render(request,'attendance/attendance_course_view.html', context)

def attendance_session_view(request,id):
    context = {}
    account_info = Account.objects.get(id=request.user.id)
    batch = Batch.objects.get(id=id)
    session = Session.objects.get(batch_of_id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.get(session_id_id=session.id, teacher_id=teacher)
    student = Student.objects.filter(batch_id = id)
    
    date = datetime.date.today()
    try:
        done = []
        att = Attendance.objects.filter(student_id__in=student,teacher_id=teacher, session_id=session,course_of=course, date=date)

        for c in att:
            done.append(c)
        a= 0
        b=0
        for present in done:
            if present.status == True:
                a= a+1
            else:
                b=b+1
            
  
        context.update({ 'att': done, 'a':a, 'b':b, })
        
    except:
        not_done = True
        context.update({ 'not_done': not_done })

    context.update({
        'current' : 'current',        
        'session': session,
        'course' : course,
        'student' : student,
        'account_info' : account_info,
        'batch': batch,})

    return render(request, 'attendance/attendance_session_view.html', context)



def attendance_present(request, id):

    account_info = Account.objects.get(id=request.user.id)
    student = Student.objects.get(id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    session = Session.objects.get(batch_of_id=student.batch.id)
    course = Course.objects.get(teacher_id_id=teacher.id,session_id_id=session.id)
    date = datetime.date.today()
    try:
        a = Attendance.objects.get(student_id=student,teacher_id=teacher, session_id=session,course_of=course,status=False, date=date)
        a.status = True
        a.save()
    except:    
        attendance = Attendance.objects.get_or_create(student_id=student,teacher_id=teacher, session_id=session,course_of=course,status=True,date=date)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def attendance_absent(request, id):

    account_info = Account.objects.get(id=request.user.id)
    student = Student.objects.get(id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    session = Session.objects.get(batch_of_id=student.batch.id)
    course = Course.objects.get(teacher_id_id=teacher.id,session_id_id=session.id)
    date = datetime.date.today()
    try:
        a = Attendance.objects.get(student_id=student,teacher_id=teacher, session_id=session,course_of=course,status=True, date=date)
        a.status = False
        a.save()

    except:
        attendance = Attendance.objects.get_or_create(student_id=student,teacher_id=teacher, session_id=session,course_of=course, date=date)
    
    print('absent')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




#Lab Attendance#

def lab_attendance_homepage(request,id):

    account_info = Account.objects.get(id=request.user.id)
    current_time = datetime.datetime.now()
    course = Course.objects.filter(session_id = id)
    session = Session.objects.filter(id = course.id)

    context = {
        'labcurrent' : 'current',
        'current_time': current_time,
        'account_info' : account_info,
    }
    return render(request, 'lab_attendance/lab_attendance_homepage.html', context)


def lab_attendance_faculty_detail(request, id):

    account_info = Account.objects.get(id=request.user.id)
    faculty_detail = Faculty.objects.get(id=id)
    batch = Batch.objects.all()

    context = {
        'labcurrent' : 'current',
        'faculty_id': faculty_detail,
        'batch': batch,
        'account_info' : account_info,
    }

    return render(request,'lab_attendance/lab_attendance_faculty.html', context)

def lab_attendance_faculty_view(request):
    
    account_info = Account.objects.get(id=request.user.id)
    teacher = Teacher.objects.get(user_id = request.user.id)
    faculty = Faculty.objects.all()

    context = {
        'labcurrent' : 'current',
        'faculty' : faculty,
        'account_info' : account_info,
    }

    return render(request,'lab_attendance/lab_attendance_faculty_view.html', context)


def lab_attendance_batch_view(request, id):
    #course = Batch.objects.filter(faculty_id=id)
    #teacher = Teacher.objects.get(user_id=request.user.id)
    #student = Student.objects.filter(batch_id = id)

    account_info = Account.objects.get(id=request.user.id)
    faculty = Faculty.objects.get(id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.filter(faculty_id=id,teacher_id_id=teacher)
    print(len(course))

    context = {
        'labcurrent' : 'current',
        'course': course,
        'teacher': teacher,
        'account_info' : account_info,
        
    }

    return render(request,'lab_attendance/lab_attendance_course_view.html', context)





def lab_attendance_group_view(request,id):
    
    account_info = Account.objects.get(id=request.user.id)
    groups = Group.objects.filter(batch__id=id)
    session = Session.objects.get(batch_of_id=id)
    sid = id
    context = {
        'labcurrent' : 'current',
        'groups' : groups,
        'session' : session,
        'sid' : sid,
        'account_info' : account_info,
    }

    return render(request,'lab_attendance/lab_attendance_group_view.html', context)



def lab_attendance_session_view(request,id,sid):
    context = {}
    sid = sid
    account_info = Account.objects.get(id=request.user.id)
    student = Student.objects.filter(group_id=id, batch_id=sid)
    session = Session.objects.get(batch_of_id=sid)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.get(session_id_id=session.id, teacher_id=teacher)
    
    date = datetime.date.today()
    try:
        done = []
        att = Lab_Attendance.objects.filter(student_id__in=student,teacher_id=teacher, session_id=session,course_of=course, date=date)

        for c in att:
            done.append(c)
        a= 0
        b=0
        for present in done:
            if present.status == True:
                a= a+1
            else:
                b=b+1
            
  
        context.update({ 'att': done, 'a':a, 'b':b, })
        
    except:
        not_done = True
        context.update({ 'not_done': not_done })

    context.update({
        'labcurrent' : 'current',        
        'session': session,
        'course' : course,
        'student' : student,
        'account_info' : account_info,
        'sid': sid,})

    return render(request, 'lab_attendance/lab_attendance_session_view.html', context)



def lab_attendance_present(request, id):


    student = Student.objects.get(id=id)


    batch = student.batch

    session = Session.objects.get(batch_of_id=batch.id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.get(session_id_id=session.id, teacher_id=teacher)
    date = datetime.date.today()
    try:
        a = Lab_Attendance.objects.get(student_id=student,teacher_id=teacher, session_id=session,course_of=course,status=False, date=date)
        a.status = True
        a.save()
    except:    
        attendance = Lab_Attendance.objects.get_or_create(student_id=student,teacher_id=teacher, session_id=session,course_of=course,status=True,date=date)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def lab_attendance_absent(request, id):

    student = Student.objects.get(id=id)


    batch = student.batch

    session = Session.objects.get(batch_of_id=batch.id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.get(session_id_id=session.id, teacher_id=teacher)
    date = datetime.date.today()
    
    try:
        a = Lab_Attendance.objects.get(student_id=student,teacher_id=teacher, session_id=session,course_of=course,status=True, date=date)
        a.status = False
        a.save()

    except:
        attendance = Lab_Attendance.objects.get_or_create(student_id=student,teacher_id=teacher, session_id=session,course_of=course, date=date)
    
    print('absent')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
