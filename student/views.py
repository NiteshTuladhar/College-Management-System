from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .models import *
from django.contrib import messages
from .forms import EditStudentForm, EditFacultyForm, EditBatchForm, EditSessionForm, EditCourseForm, EditTeacherForm, EditGroupForm
from .models import Account
from notices.models import NoticeBoard
from django.contrib import messages
from assignments.models import *

from InternalMarksPrediction.models import TotalMarks, WeeklyInternalMaks, InternalMaks

from .attachment_mail import Custom_attachmail

from attendance.models import *
from assessment.models import *
import _datetime
from django.db.models import Min
from InternalMarksPrediction.algorithm import algorithm

# Create your views here.


def edit_student_form(request):

    account_info = Account.objects.get(id=request.user.id)
    account = Account.objects.latest('id')
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    form = EditStudentForm()
    if request.method == "POST":
        form = EditStudentForm(request.POST or None)
        print(account.full_name)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = account
            print(form.user)
            form.save()
            messages.success(request, "Student Has been added.")
            return redirect('dashboard')
    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'add_form/student_edit_form.html', context)


def edit_faculty_form(request):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    form = EditFacultyForm()
    if request.method == "POST":
        form = EditFacultyForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty Has Been Added.")
            return redirect('faculty_view')

    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'add_form/faculty_edit_form.html', context)


def edit_group_form(request):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    form = EditGroupForm()
    if request.method == "POST":
        form = EditGroupForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Group Has Been Added.")
            return redirect('faculty_view')

    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'add_form/faculty_edit_form.html', context)


def faculty_view(request):
    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()

    faculty = Faculty.objects.all()
    group = Group.objects.all()

    context = {
        'faculty_current': 'current',
        'faculty': faculty,
        'group': group,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'view/faculty_view.html', context)


def faculty_detail(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    faculty_detail = Faculty.objects.get(id=id)
    batch = Batch.objects.filter(faculty_id=faculty_detail.id)

    context = {
        'faculty_current': 'current',
        'faculty_id': faculty_detail,
        'batch': batch,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'details/faculty_details.html', context)


def edit_batch_form(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    faculty = Faculty.objects.get(id=id)
    form = EditBatchForm()
    if request.method == "POST":
        form = EditBatchForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Batch Has Been Added.")
            return redirect('faculty_detail', faculty.id)
    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'add_form/batch_edit_form.html', context)


# SESSION VIEW #

def session_view(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    session = Session.objects.filter(batch_of_id=id)
    batch = Batch.objects.get(id=id)
    context = {'faculty_current': 'current', 'session': session,
               'account_info': account_info, 'batch': batch}

    return render(request, 'view/session_view.html', context)


def add_session(request, id):
    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    batch = Batch.objects.get(id=id)
    form = EditSessionForm()
    if request.method == "POST":
        form = EditSessionForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Session Has Been Added")
            return redirect('session_view', batch.id)
    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'add_form/session_edit_form.html', context)


def edit_session(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    session = Session.objects.get(id=id)

    form = EditSessionForm(request.POST or None, instance=session)

    if form.is_valid():
        form.save()
        messages.success(request, "Session Has Been Added.")
        return redirect('session_view', session.batch_of.id)

    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'edit_forms/edit_in_session.html', context)


def delete_session(request, id):

    session = Session.objects.get(id=id)
    session.delete()
    messages.warning(request, "Session Has Been Removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#COURSE VIEW #

def course_view(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    course = Course.objects.filter(session_id_id=id)
    session = Session.objects.get(id=id)

    context = {'faculty_current': 'current', 'course': course,
               'session': session, 'account_info': account_info}

    return render(request, 'view/course_view.html', context)


def add_course(request, id):
    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    session = Session.objects.get(id=id)
    form = EditCourseForm()
    if request.method == "POST":
        form = EditCourseForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Course Has Been Added.")
            return redirect('course_view', session.id)
    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'add_form/course_edit_form.html', context)


def edit_course(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    course = Course.objects.get(id=id)

    form = EditCourseForm(request.POST or None, instance=course)

    if form.is_valid():
        form.save()
        messages.success(request, "Course Has Been Updated.")
        return redirect('course_view', course.session_id.id)

    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'edit_forms/edit_in_course.html', context)


def delete_course(request, id):

    course = Course.objects.get(id=id)
    course.delete()
    messages.warning(request, "Course Has Been Removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# STUDENT VIEW#

def student_view(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    student = Student.objects.filter(batch_id=id)

    context = {
        'std_current': 'current',
        'student': student,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'view/student_view.html', context)


def edit_student(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    student = Student.objects.get(id=id)

    form = EditStudentForm(request.POST or None, instance=student)

    if form.is_valid():
        form.save()
        messages.success(request, "Student Has Been Updated.")
        return redirect('student_view', student.batch.id)

    context = {
        'std_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'edit_forms/edit_in_student.html', context)


def remove_student(request, id):

    student = Student.objects.get(id=id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    student.delete()
    messages.warning(request, "Student Has Been Removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def edit_individual_faculty(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    faculty = Faculty.objects.get(id=id)

    form = EditFacultyForm(request.POST or None, instance=faculty)

    if form.is_valid():
        form.save()
        messages.success(request, "Faculty Has Been Updated.")
        return redirect('faculty_view')

    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'edit_forms/edit_in_faculty.html', context)


def edit_individual_group(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    group = Group.objects.get(id=id)

    form = EditGroupForm(request.POST or None, instance=group)

    if form.is_valid():
        form.save()
        messages.success(request, "Group Has Been Updated.")
        return redirect('faculty_view')

    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'edit_forms/edit_in_faculty.html', context)


def delete_faculty(request, id):

    faculty = Faculty.objects.get(id=id)
    faculty.delete()
    messages.warning(request, "Faculty Has Been Removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_group(request, id):

    group = Group.objects.get(id=id)
    group.delete()
    messages.warning(request, "Group Has Been Removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def edit_individual_batch(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    batch = Batch.objects.get(id=id)

    form = EditBatchForm(request.POST or None, instance=batch)

    if form.is_valid():
        form.save()
        messages.success(request, "Batch Has Been Updated.")
        return redirect('faculty_detail', batch.faculty.id)

    context = {
        'faculty_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'edit_forms/edit_in_detail.html', context)


def delete_batch(request, id):

    batch = Batch.objects.get(id=id)
    batch.delete()
    messages.warning(request, "Batch Has Been Removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def faculty_student_view(request):
    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()

    faculty = Faculty.objects.all()

    context = {
        'std_current': 'current',
        'faculty': faculty,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'edit_student/faculty_student_view.html', context)


def faculty_batch_view(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    faculty_detail = Faculty.objects.get(id=id)
    batch = Batch.objects.filter(faculty_id=faculty_detail.id)

    context = {
        'std_current': 'current',
        'faculty_id': faculty_detail,
        'batch': batch,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'edit_student/faculty_batch_view.html', context)


def teacher_view(request):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    teacher = Teacher.objects.all()

    context = {
        'teach_current': 'current',
        'teacher': teacher,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'edit_teacher/faculty_teacher_view.html', context)


def edit_teacher(request, id):

    account_info = Account.objects.get(id=request.user.id)
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    teacher = Teacher.objects.get(id=id)

    form = EditTeacherForm(request.POST or None, instance=teacher)

    if form.is_valid():
        form.save()
        messages.success(request, "Teacher Has Been Updated.")
        return redirect('teacher_view')

    context = {
        'teach_current': 'current',
        'form': form,
        'account_info': account_info,
        'notice_count': notices_count,
    }

    return render(request, 'edit_forms/edit_in_student.html', context)


def remove_teacher(request, id):

    teacher = Teacher.objects.get(id=id)
    teacher.delete()
    messages.warning(request, "Teacher Has Been Removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def edit_session_status(request):
    notices_count = NoticeBoard.objects.all().order_by('-notice_date').count()
    account_info = Account.objects.get(id=request.user.id)
    session = Session.objects.all()
    faculty = Faculty.objects.all()

    context = {'account_info': account_info, 'notice_count': notices_count,
               's_current': 'current', 'session': session, 'faculty': faculty}

    return render(request, 'edit_session/edit_session_status.html', context)


def change_session_status(request, id):

    session = Session.objects.get(id=id)

    if(session.active == 'Active'):

        session.active = 'Inactive'
        messages.error(request, "Session Status Has Been Updated To Inactive.")

    elif(session.active == 'Inactive'):

        session.active = 'Active'
        messages.success(request, "Session Status Has Been Updated To Active.")

    else:
        pass

    session.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Student_homepage Starts here

def student_homepage(request):

    account = Student.objects.get(user_id=request.user.id)
    session = Session.objects.get(batch_of_id=account.batch.id)
    course = Course.objects.filter(session_id_id=session.id)
    print(course)
    active_show = 'active show'
    context = {
        'course': course,
        'account': account,
        'active_show': active_show
    }
    return render(request, 'student_homepage.html', context)


def student_notice_board(request):

    student_info = Student.objects.get(user_id=request.user.id)
    session = Session.objects.get(batch_of_id=student_info.batch.id)

    notices = NoticeBoard.objects.filter(
        semester__id=session.id, type='Notice')

    announcements = NoticeBoard.objects.filter(
        semester__id=session.id, type='Announcement')

    active_show = 'active show'
    print(announcements)
    context = {

        'notices': notices,
        'announcements': announcements,
        'noticeshow': active_show,
    }

    return render(request, 'students/student_notice.html', context)


def student_assignment(request):

    student_info = Student.objects.get(user_id=request.user.id)
    session = Session.objects.get(batch_of_id=student_info.batch.id)

    batch_of = student_info.batch

    try:

        assignment_detail = AssignmentTopView.objects.filter(
            session_id=session.id)

    except:

        assignment_detail = "Nill"

    assignment_active_show = 'active show'
    context = {
        'assignment_active_show': assignment_active_show,
        'assignment_detail': assignment_detail,
    }
    return render(request, 'students/student_assignment.html', context)


def student_assignment_details(request, id):

    assignment_topview_detail = AssignmentTopView.objects.get(id=id)
    assignment_details = Assignment.objects.get(
        assignment_name__id=id, student_id__user_id=request.user.id)

    context = {
        'atd': assignment_topview_detail,
        'ad': assignment_details,
    }
    return render(request, 'students/student_assignment_details.html', context)


def submit_assignment(request, id):

    teacher_info = AssignmentTopView.objects.get(id=id)
    s_assignment = Assignment.objects.get(
        student_id__user_id=request.user.id, assignment_name=teacher_info)

    print('---No------ Ajax')
    if request.is_ajax():
        print('---yes------ Ajax')
        if request.method == 'POST':

            file = request.FILES['file']

            s_assignment.assignment_file = file

            s_assignment.submitted = 'Submitted'

            s_assignment.save()

            student_name = s_assignment.student_id.user.full_name
            student_subject = teacher_info.course_id.course_name
            student_faculty = s_assignment.student_id.batch.faculty
            student_sem = teacher_info.course_id.session_id
            host_email = teacher_info.teacher_id.user.email

            mail = Custom_attachmail('mail/send_assignment_file_email.html', 'Assignment Submission', [host_email], student_name=student_name,
                                     student_subject=student_subject, student_faculty=student_faculty, student_sem=student_sem, file=file)

            mail.push(request)
            messages.success(
                request, 'Your assignments has been submitted successfully')

    context = {}

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#LAB ASSIGNMENT#

def student_lab_assignment(request):

    student_info = Student.objects.get(user_id=request.user.id)
    session = Session.objects.get(batch_of_id=student_info.batch.id)

    batch_of = student_info.batch

    try:

        lab_assignment_detail = LabAssignmentTopView.objects.filter(
            session_id=session.id, group=student_info.group)

    except:

        lab_assignment_detail = "Nill"

    lab_assignment_active_show = 'active show'
    context = {
        'lab_assignment_active_show': lab_assignment_active_show,
        'lab_assignment_detail': lab_assignment_detail,
    }

    return render(request, 'students/student_lab_assignment.html', context)


def student_lab_assignment_details(request, id):

    student = Student.objects.get(user_id=request.user.id)
    lab_assignment_topview_detail = LabAssignmentTopView.objects.get(id=id)
    lab_assignment_details = LabAssignment.objects.get(
        assignment_name__id=id, student_id__user_id=request.user.id)

    context = {
        'student': student,
        'atd': lab_assignment_topview_detail,
        'ad': lab_assignment_details,
    }
    return render(request, 'students/student_lab_assignment_details.html', context)


def submit_lab_assignment(request, id):

    s_assignment = LabAssignment.objects.get(
        student_id__user_id=request.user.id)
    teacher_info = LabAssignmentTopView.objects.get(id=id)

    if request.method == 'POST':

        file = request.FILES['file']

        s_assignment.lab_assignment_file = file

        s_assignment.submitted = 'Submitted'

        s_assignment.save()

        student_name = s_assignment.student_id.user.full_name
        student_subject = teacher_info.course_id.course_name
        student_faculty = s_assignment.student_id.batch.faculty
        student_sem = teacher_info.course_id.session_id

        student = Student.objects.get(user_id=request.user.id)
        student_group = student.group.group_name

        host_email = teacher_info.teacher_id.user.email

        print(host_email)
        print('====================================================email')

        mail = Custom_attachmail('mail/send_lab_assignment_file_email.html', 'Lab Assignment Submission', [host_email], student_name=student_name,
                                 student_subject=student_subject, student_faculty=student_faculty, student_sem=student_sem, student_group=student_group, file=file)

        mail.push(request)
        messages.success(
            request, 'Your lab assignments has been submitted successfully')

    context = {}

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def student_dashboard(request):

    account_info = Account.objects.get(id=request.user.id)
    account = Student.objects.get(user_id=request.user.id)
    session = Session.objects.get(batch_of_id=account.batch.id)
    course = Course.objects.filter(session_id_id=session.id)
    int_weekly_marks = WeeklyInternalMaks.objects.filter(
        student=account).order_by('-date_created')

    add_overal_present_percent = 0
    total_lab_attendace_course = 0
    add_overal_lab_present_percent=0
    
    for t in course:
        try:
            total_present = Attendance.objects.filter(
                student_id=account, course_of=t, status=True).count()
            total_absent = Attendance.objects.filter(
                student_id=account, course_of=t, status=False).count()
            total_attendace = Attendance.objects.filter(
                student_id=account, course_of=t).count()
            overal_present_percent = (total_present/total_attendace) * 100
            add_overal_present_percent += overal_present_percent

        except:
            add_overal_present_percent += 100
    overall_class_attendance = add_overal_present_percent/course.count()

   
    for t in course:
        try:
            total_lab_present = Lab_Attendance.objects.filter(
                student_id=account, course_of=t, status=True).count()
            total_lab_absent = Lab_Attendance.objects.filter(
                student_id=account, course_of=t, status=False).count()
            total_lab_attendace = Lab_Attendance.objects.filter(
                student_id=account, course_of=t).count()
            overal_lab_present_percent = (
                total_lab_present/total_lab_attendace) * 100
            add_overal_lab_present_percent += overal_lab_present_percent

        except:
            add_overal_lab_present_percent += 100
    overall_class_lab_attendance = add_overal_lab_present_percent/course.count()

    avg_perc = (overall_class_attendance + overall_class_lab_attendance)/2
 
    course_color = CourseColor.objects.filter(course__in=course)
    total = 0
    try:
        for c in course:
            int_weekly_marks_course = WeeklyInternalMaks.objects.filter(
                student=account, course=c).order_by('-week_created')[0]
            total += int_weekly_marks_course.daily_internal_marks
        avg = total / (course.count())

    except:

        avg = 0

    course_count = course.count()
    active_show = 'active show'
    context = {
        'course': course,
        'account': account,
        'account_info': account_info,
        'active_show': active_show,
        'int_weekly_marks': int_weekly_marks,
        'course_color': course_color,
        'homecurrent': 'current',
        'course_count': course_count,
        'total': avg,
        'session': session,
        'avg_perc': avg_perc,

    }

    return render(request, 'students/student_dashboard.html', context)


def student_course_detail(request, id):

    course_detail = Course.objects.get(id=id)
    print(course_detail)

    # course_detail
    course_detail = Course.objects.get(id=id)
    student_info = Student.objects.get(user_id=request.user.id)

    # attendance
    total_attendance = Attendance.objects.filter(
        course_of_id=id, student_id_id=student_info.id).count()
    attendance_present = Attendance.objects.filter(
        course_of_id=id, student_id_id=student_info.id, status=True).count()
    attendance_absent = Attendance.objects.filter(
        course_of_id=id, student_id_id=student_info.id, status=False).count()

    try:
        percentage = (attendance_present/total_attendance)*100
    except:
        percentage = 0

    # assignment
    assignment = AssignmentTopView.objects.filter(course_id_id=id)
    assignment_submitted = Assignment.objects.filter(
        assignment_name__in=assignment, student_id_id=student_info.id, submitted='Submitted').count()
    assignment_not_submitted = Assignment.objects.filter(
        assignment_name__in=assignment, student_id_id=student_info.id, submitted='Not Submitted').count()
    total_assignment = AssignmentTopView.objects.filter(
        course_id_id=id).count()
    try:
        assignment_percentage = (assignment_submitted/total_assignment)*100
    except:
        assignment_percentage = 0

    # lab_attendance
    lab_total_attendance = Lab_Attendance.objects.filter(
        course_of_id=id, student_id_id=student_info.id).count()
    lab_attendance_present = Lab_Attendance.objects.filter(
        course_of_id=id, student_id_id=student_info.id, status=True).count()
    lab_attendance_absent = Lab_Attendance.objects.filter(
        course_of_id=id, student_id_id=student_info.id, status=False).count()

    try:
        lab_percentage = (lab_attendance_present/lab_total_attendance)*100
    except:
        lab_percentage = 0

    # lab_assignment
    student_group = student_info.group
    assignment = LabAssignmentTopView.objects.filter(
        course_id_id=id, group=student_group)
    lab_assignment_submitted = LabAssignment.objects.filter(
        assignment_name__in=assignment, student_id_id=student_info.id, submitted='Submitted').count()
    lab_assignment_not_submitted = LabAssignment.objects.filter(
        assignment_name__in=assignment, student_id_id=student_info.id, submitted='Not Submitted').count()
    total_lab_assignment = LabAssignmentTopView.objects.filter(
        course_id_id=id, group=student_group).count()
    try:
        lab_assignment_percentage = (
            lab_assignment_submitted/total_lab_assignment)*100
    except:
        lab_assignment_percentage = 0

    # assessment
    # class-assessment
    try:
        class_assesment = AssessmentTopView.objects.get(
            course_name_id=id, assessment_type='Class Test')
        class_assesment_marks = Assesment.objects.get(
            assesment_name=class_assesment, student_name_id=student_info.id)
        class_assessment_marks = class_assesment_marks.marks

    except:
        class_assessment_marks = 0

    # Mid-Assessment
    try:
        mid_assesment = AssessmentTopView.objects.get(
            course_name_id=id, assessment_type='Mid-Term')
        mid_assessment_marks = Assesment.objects.get(
            assesment_name=mid_assesment, student_name_id=student_info.id)
        mid_assessment_marks = mid_assessment_marks.marks
    except:
        mid_assessment_marks = 0
    # Final-Assessment
    try:
        final_assesment = AssessmentTopView.objects.get(
            course_name_id=id, assessment_type='Final-Term')
        final_assessment_marks = Assesment.objects.get(
            assesment_name=final_assesment, student_name_id=student_info.id)
        final_assessment_marks = final_assessment_marks.marks

    except:
        final_assessment_marks = 0

    # INTERNAL MARKS
    # Attendance
    try:
        internal_attendance = (attendance_present/total_attendance) * 1.5
        internal_lab_attendance = (
            lab_attendance_present/lab_total_attendance)*1.5
    except:
        internal_attendance = 0
        internal_lab_attendance = 0
    # Assessment
    # Class-Assessment

    internal_class_assessment = (class_assessment_marks/20)*1

    # Mid-Term Assessment
    internal_mid_assessment = mid_assessment_marks
    if internal_mid_assessment > 80:
        internal_mid_assessment = 4
    elif internal_mid_assessment > 60:
        internal_mid_assessment = 3
    elif internal_mid_assessment > 40:
        internal_mid_assessment = 2
    else:
        internal_mid_assessment = 0

    # Final-Term Assessment
    internal_final_assessment = final_assessment_marks
    if internal_final_assessment > 80:
        internal_final_assessment = 7
    elif internal_final_assessment > 60:
        internal_final_assessment = 6
    elif internal_final_assessment > 40:
        internal_final_assessment = 4
    else:
        internal_final_assessment = 0

    # ASSIGNMENT
    # Class Assignment and Lab Assignment
    try:
        internal_class_assignment = (assignment_submitted/total_assignment)*10
        internal_lab_class_assignment = (
            lab_assignment_submitted/total_lab_assignment)*10
        total_assignment_marks = (
            (internal_class_assignment+internal_lab_class_assignment)/20)*3
    except:
        internal_class_assignment = 0
        internal_lab_class_assignment = 0
        total_assignment_marks = 0

    # CLASS ACTIVITY
    internal_class_activity = float(
        (internal_class_assignment+internal_lab_class_assignment+lab_attendance_present+attendance_present)/23)*3

    # Sum
    internal_marks = internal_attendance + internal_lab_attendance + internal_mid_assessment + \
        internal_final_assessment + total_assignment_marks + internal_class_activity

    context = {
        'course_detail': course_detail,
        'attendance_present': attendance_present,
        'attendance_absent': attendance_absent,
        'total_attendance': total_attendance,
        'percentage': percentage,
        'total_assignment': total_assignment,
        'assignment_submitted': assignment_submitted,
        'assignment_not_submitted': assignment_not_submitted,
        'assignment_percentage': assignment_percentage,
        'lab_total_attendance': lab_total_attendance,
        'lab_attendance_present': lab_attendance_present,
        'lab_attendance_absent': lab_attendance_absent,
        'lab_percentage': lab_percentage,
        'lab_assignment_submitted': lab_assignment_submitted,
        'lab_assignment_not_submitted': lab_assignment_not_submitted,
        'total_lab_assignment': total_lab_assignment,
        'lab_assignment_percentage': lab_assignment_percentage,
        'class_assessment_marks': class_assessment_marks,
        'mid_assessment_marks': mid_assessment_marks,
        'final_assessment_marks': final_assessment_marks,
        'active_show': 'active show',
        'internal_marks': internal_marks,



    }

    return render(request, 'students/student_course_detail.html', context)


def student_profile(request):
    student_account = request.user
    student_email = student_account.email
    student_dob = student_account.date_of_birth
    student_address = student_account.address
    student_contact_number = request.user.contact_no
    student_model = Student.objects.get(user_id=request.user.id)
    roll_no = student_model.roll_no
    group = student_model.group
    fathers_name = student_model.fathers_name
    mothers_name = student_model.mothers_name

    student_active = 'active show'

    context = {
        'student_active': student_active,
        'student_account': student_account,
        'student_email': student_email,
        'student_dob': student_dob,
        'student_address': student_address,
        'student_contact_number': student_contact_number,
        'roll_no': roll_no,
        'group': group,
        'fathers_name': fathers_name,
        'mothers_name': mothers_name,

    }

    return render(request, 'students/student_profile.html', context)


def studentReport(request):

    student = Student.objects.get(user=request.user)
    intmarks = InternalMaks.objects.filter(student=student)

    total_marks = 0
    credit = 0
    for i in intmarks:

        total_marks += i.calculateInternalMarks
        credit += i.course.credit

    # For Storing the total marks of student
    batch_of_student = student.batch
    session_of_student = Session.objects.get(batch_of_id=batch_of_student.id)
    course_of_student = Course.objects.filter(
        session_id_id=session_of_student.id)

    total_attendance_cal = 0
    total_assignment_cal = 0
    total_lab_attendance_cal = 0
    total_lab_assignment_cal = 0
    total_class_assesment_cal = 0
    total_mid_assessment_cal = 0
    total_final_assessment_cal = 0
    for course in course_of_student:
        # attendance
        total_attendance = Attendance.objects.filter(
            course_of_id=course.id, student_id_id=student.id).count()
        attendance_present = Attendance.objects.filter(
            course_of_id=course.id, student_id_id=student.id, status=True).count()
        attendance_absent = Attendance.objects.filter(
            course_of_id=course.id, student_id_id=student.id, status=False).count()

        try:
            percentage = (attendance_present/total_attendance)*100
            total_attendance_cal += percentage

        except:
            total_attendance_cal += 100

        assignment = AssignmentTopView.objects.filter(course_id_id=course.id)
        assignment_submitted = Assignment.objects.filter(
            assignment_name__in=assignment, student_id_id=student.id, submitted='Submitted').count()
        assignment_not_submitted = Assignment.objects.filter(
            assignment_name__in=assignment, student_id_id=student.id, submitted='Not Submitted').count()
        total_assignment = AssignmentTopView.objects.filter(
            course_id_id=course.id).count()
        try:
            assignment_percentage = (assignment_submitted/total_assignment)*100
            total_assignment_cal += assignment_percentage
        except:
            total_assignment_cal += 100

        # lab_attendance
        lab_total_attendance = Lab_Attendance.objects.filter(
            course_of_id=course.id, student_id_id=student.id).count()
        lab_attendance_present = Lab_Attendance.objects.filter(
            course_of_id=course.id, student_id_id=student.id, status=True).count()
        lab_attendance_absent = Lab_Attendance.objects.filter(
            course_of_id=course.id, student_id_id=student.id, status=False).count()

        try:
            lab_percentage = (lab_attendance_present/lab_total_attendance)*100
            total_lab_attendance_cal += lab_percentage
        except:
            total_lab_attendance_cal += 100

        # lab_assignment
        student_group = student.group
        assignment = LabAssignmentTopView.objects.filter(
            course_id_id=course.id, group=student_group)
        lab_assignment_submitted = LabAssignment.objects.filter(
            assignment_name__in=assignment, student_id_id=student.id, submitted='Submitted').count()
        lab_assignment_not_submitted = LabAssignment.objects.filter(
            assignment_name__in=assignment, student_id_id=student.id, submitted='Not Submitted').count()
        total_lab_assignment = LabAssignmentTopView.objects.filter(
            course_id_id=course.id, group=student_group).count()
        try:
            lab_assignment_percentage = (
                lab_assignment_submitted/total_lab_assignment)*100
            total_lab_assignment_cal += lab_assignment_percentage
        except:
            total_lab_assignment_cal += 100

         # assessment
        # class-assessment
        try:
            class_assesment = AssessmentTopView.objects.get(
                course_name_id=course.id, assessment_type='Class Test')
            class_assesment_marks = Assesment.objects.get(
                assesment_name=class_assesment, student_name_id=student.id)
            class_assessment_marks = class_assesment_marks.marks
            marks_conversion = class_assessment_marks*5
            total_class_assesment_cal += marks_conversion

        except:
            total_class_assesment_cal += 100

        # Mid-Assessment
        try:
            mid_assesment = AssessmentTopView.objects.get(
                course_name_id=course.id, assessment_type='Mid-Term')
            mid_assessment_marks = Assesment.objects.get(
                assesment_name=mid_assesment, student_name_id=student.id)
            mid_assessment_marks = mid_assessment_marks.marks
            total_mid_assessment_cal += mid_assessment_marks
        except:
            total_mid_assessment_cal += 100

        # Final-Assessment
        try:
            final_assesment = AssessmentTopView.objects.get(
                course_name_id=course.id, assessment_type='Final-Term')
            final_assessment_marks = Assesment.objects.get(
                assesment_name=final_assesment, student_name_id=student.id)
            final_assessment_marks = final_assessment_marks.marks
            total_final_assessment_cal += final_assessment_marks

        except:
            total_final_assessment_cal += 100

    grandtotalattendance = total_attendance_cal/course_of_student.count()
    grandtotalassignment = total_assignment_cal/course_of_student.count()
    grandtotallabattendance = total_lab_attendance_cal/course_of_student.count()
    grandtotallabassignment = total_lab_assignment_cal/course_of_student.count()
    grandtotalclassassesement = total_class_assesment_cal/course_of_student.count()
    grandtotalmidassessment = total_mid_assessment_cal/course_of_student.count()
    grandtotalfinalassessment = total_final_assessment_cal/course_of_student.count()

    totalmarks, created = TotalMarks.objects.get_or_create(user_id=student.id)
    totalmarks.total_attendance_marks = grandtotalattendance
    totalmarks.total_assignment_marks = grandtotalassignment
    totalmarks.total_lab_attendance_marks = grandtotallabattendance
    totalmarks.total_lab_assignment_marks = grandtotallabassignment
    totalmarks.total_class_assesment_marks = grandtotalclassassesement
    totalmarks.total_mid_assessment_marks = grandtotalmidassessment
    totalmarks.total_final_assessment_marks = grandtotalfinalassessment
    totalmarks.save()

    algo = algorithm(request)

    context = {
        'intmarks': intmarks,
        'total_marks': total_marks,
        'credit': credit,
        'reportcurrent': 'current',
        'algo': algo,
        'course_of_student' : course_of_student
    }

    return render(request, 'students/student_report.html', context)
