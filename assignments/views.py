from django.shortcuts import render, redirect, HttpResponseRedirect
from assignments.models import *
from student.models import *
from .forms import CreateAssignment, CreateLabAssignment
import datetime
from django.contrib import messages
# Create your views here.
def assignment_home(request):

    account_info = Account.objects.get(id=request.user.id)
    teacher = Teacher.objects.get(user_id = request.user.id)
    faculty = Faculty.objects.all()
    context = {
        'assigncurrent' : 'current',
        'faculty': faculty,
        'account_info' : account_info
    }

    return render(request,'assignment/assignment_home.html', context)

def assignment_batch(request, id):

    account_info = Account.objects.get(id=request.user.id)
    batch = Batch.objects.filter(faculty_id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    context = {
        'assigncurrent' : 'current',
        'account_info' : account_info,
        'batch': batch,
        'teacher': teacher,
    }

    return render(request, 'assignment/assignment_batch_view.html', context)


def assignment_session_view(request, id):
    context = {}

    account_info = Account.objects.get(id=request.user.id)
    session = Session.objects.get(batch_of_id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.filter(session_id_id=session.id, teacher_id=teacher)
    course_length = len(course)
    if course_length == 0:
        return redirect('errorpage')
    else:
        student = Student.objects.filter(batch_id = id)
        assignments = AssignmentTopView.objects.filter(teacher_id=teacher, course_id__in=course, session_id=session)
        context.update({'assignment': assignments,'session':session,'assigncurrent' : 'current',})
    context.update({'account_info':account_info})


    
    return render(request, 'assignment/assignment_session_view.html', context)



def create_assignment(request, id):

    account_info = Account.objects.get(id=request.user.id)
    student = Student.objects.filter(batch_id=id)
    session = Session.objects.get(batch_of_id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.get(session_id_id=session.id, teacher_id=teacher)
    form = CreateAssignment()
    if request.method == "POST":
        form = CreateAssignment(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.teacher_id = teacher
            form.course_id = course
            form.session_id = session
            form.save()
            messages.success(request,"Assignment Has Been Created.")
            date = datetime.date.today()
            assignment_detail = AssignmentTopView.objects.get(id=form.id)
            for s in student:
                checks = Assignment(student_id_id=s.id, submitted_on=date, assignment_name=assignment_detail)
                checks.submitted=check[1][1]
                checks.save()
            return redirect('assignment_session_view', session.batch_of.id)


    context = {
        'assigncurrent' : 'current',
        'course': course,
        'form': form,
        'account_info' : account_info,
    }
    return render(request,'assignment/create_assignment.html', context)



def assignment_check_view(request, id):
    context = {}

    account_info = Account.objects.get(id=request.user.id)
    assignment_detail = AssignmentTopView.objects.get(id=id)
    assignment_id = assignment_detail.id
    sid = assignment_detail.session_id
    batch = sid.batch_of
    students = Student.objects.filter(batch=batch)

    try:

        checks = Assignment.objects.filter(assignment_name=assignment_detail)
        
        if checks:
            context.update({'checks': checks})

        else:
            unchecked = True
            print(unchecked)
            context.update({'unchecked': unchecked})
    except:
        pass

    context.update({

        'assigncurrent' : 'current',
        'ass':assignment_detail,
        'students': students,
        'ids':assignment_id,
        'account_info' : account_info,
        'batch' : batch,

    })
    return render(request,'assignment/check_assignment.html', context)



def assignment_done(request,id, ids, num):


    if (num<0 or num>2):
        return redirect('error.html')

    else:
        try:
            student = Student.objects.get(id=id)
            assignment_detail = AssignmentTopView.objects.get(id=ids)
            checks = Assignment.objects.get(student_id=student, assignment_name=assignment_detail)
            if checks.submitted == 'Submitted':
                checks.submitted = check[num][1]
                checks.save()
            elif checks.submitted == 'Not Submitted':
                checks.submitted = check[num][1]
                checks.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        except:
            student = Student.objects.get(id=id)
            date = datetime.date.today()
            assignment_detail= AssignmentTopView.objects.get(id=ids)
            print(assignment_detail)
            checks = Assignment(student_id=student, submitted_on=date, assignment_name=assignment_detail)
            checks.submitted=check[num][1]
            checks.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def assignment_edit(request,id):

    account_info = Account.objects.get(id=request.user.id)
    assignment_detail = AssignmentTopView.objects.get(id=id)

    session_id = assignment_detail.session_id
    print(assignment_detail)

    form = CreateAssignment(request.POST or None,instance=assignment_detail)
    if form.is_valid():
        form.save()
        messages.success(request,"Assignment Has Been Updated Successfully.")
        return redirect('assignment_session_view', session_id.batch_of.id)

    
    context = {

        'assigncurrent' : 'current',
        'form' : form,
        'account_info':account_info,
    }
    return render(request,'assignment/edit_assignment.html',context)



def assignment_delete(request,id):

    assignment_detail = AssignmentTopView.objects.get(id=id)
    assignment_detail.delete()
    messages.warning(request,"Assignment Has Been Deleted.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





#LAB ASSIGNMENT VIEW#

def lab_assignment_home(request):

    account_info = Account.objects.get(id=request.user.id)
    teacher = Teacher.objects.get(user_id = request.user.id)
    faculty = Faculty.objects.all()

    context = {
        'assignlabcurrent' : 'current',
        'faculty': faculty,
        'account_info':account_info,
    }

    return render(request,'lab_assignment/lab_assignment_home.html', context)



def lab_assignment_batch(request, id):

    account_info = Account.objects.get(id=request.user.id)
    batch = Batch.objects.filter(faculty_id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.filter(faculty_id=id,teacher_id_id=teacher)
    context = {
        'assignlabcurrent' : 'current',
        'batch': batch,
        'teacher': teacher,
        'account_info':account_info,
        'course' : course,
    }

    return render(request, 'lab_assignment/lab_assignment_batch_view.html', context)



def lab_assignment_group(request,id):

    account_info = Account.objects.get(id=request.user.id)
    groups = Group.objects.filter(batch__id=id)
    session = Session.objects.get(batch_of_id=id)
    sid = id
    context = {
        'assignlabcurrent' : 'current',
        'groups' : groups,
        'session' : session,
        'sid' : sid,
        'account_info' : account_info,
    }

    return render(request,'lab_assignment/lab_assignment_group_view.html', context)



def lab_assignment_session_view(request,id,sid):
    context = {}

    account_info = Account.objects.get(id=request.user.id)
    session = Session.objects.get(batch_of_id=sid)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.filter(session_id_id=session.id, teacher_id=teacher)
    group = Group.objects.get(id=id).id
    course_length = len(course)
    if course_length == 0:
        return redirect('errorpage')
    else:
        student = Student.objects.filter(batch_id = id)
        assignments = LabAssignmentTopView.objects.filter(teacher_id=teacher, course_id__in=course, session_id=session, group=group)

    context.update({'assignment': assignments,'session':session,'account_info':account_info,'group' : group,'assignlabcurrent' : 'current'})

    
    return render(request, 'lab_assignment/lab_assignment_session_view.html', context)




def create_lab_assignment(request,gid,id):

    account_info = Account.objects.get(id=request.user.id)
    student = Student.objects.filter(batch_id=id,group_id=gid)
    group = Group.objects.get(id=gid, batch__id=id)
    session = Session.objects.get(batch_of_id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.get(session_id_id=session.id, teacher_id=teacher)


    print(group)
    print(session)
    print(session.batch_of)
    print(course)

    form = CreateLabAssignment()
    if request.method == "POST":
        form = CreateLabAssignment(request.POST or None)


        if form.is_valid():
            form = form.save(commit=False)
            form.teacher_id = teacher
            form.course_id = course
            form.session_id = session
            form.group = group
            form.save()
            messages.success(request,"LabAssignment Has Been Created.")
            date = datetime.date.today()
            assignment_detail = LabAssignmentTopView.objects.get(id=form.id)
            for s in student:
                checks = LabAssignment(student_id_id=s.id, submitted_on=date, assignment_name=assignment_detail)
                checks.submitted=check[1][1]
                checks.save()
            return redirect('lab_assignment_session_view', gid, session.batch_of.id)
    context = {
        'assignlabcurrent' : 'current',
        'group' : group,
        'course': course,
        'form': form,
        'account_info':account_info,
    }
    return render(request,'lab_assignment/create_lab_assignment.html', context)



def lab_assignment_check_view(request, id, gid):
    context = {}

    account_info = Account.objects.get(id=request.user.id)
    assignment_detail = LabAssignmentTopView.objects.get(id=id)
    group = Group.objects.get(id=gid).id
    assignment_id = assignment_detail.id
    sid = assignment_detail.session_id
    batch = sid.batch_of
    students = Student.objects.filter(batch=batch, group_id=gid)
    try:

        checks = LabAssignment.objects.filter(assignment_name=assignment_detail)
        
        if checks:
            context.update({'checks': checks})
            print('-------------ok-------------------')
        else:
            unchecked = True
            print(unchecked)
            context.update({'unchecked': unchecked})
    except:
        pass

    context.update({
        'assignlabcurrent' : 'current',
        'ass':assignment_detail,
        'students': students,
        'ids':assignment_id,
        'account_info':account_info,
        'batch' : batch,
        'group' : group,

    })
    return render(request,'lab_assignment/lab_assignment_check_view.html', context)



def lab_assignment_done(request,id, ids, num):

    
    if (num<0 or num>2):
        return redirect('error.html')

    else:
        try:
            student = Student.objects.get(id=id)
            assignment_detail = LabAssignmentTopView.objects.get(id=ids)
            checks = LabAssignment.objects.get(student_id=student, assignment_name=assignment_detail)
            if checks.submitted == 'Submitted':
                checks.submitted = check[num][1]
                checks.save()
            elif checks.submitted == 'Not Submitted':
                checks.submitted = check[num][1]
                checks.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        except:
            student = Student.objects.get(id=id)
            date = datetime.date.today()
            assignment_detail= LabAssignmentTopView.objects.get(id=ids)
            print(assignment_detail)
            checks = LabAssignment(student_id=student, submitted_on=date, assignment_name=assignment_detail)
            checks.submitted=check[num][1]
            checks.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def lab_assignment_edit(request,id):

    account_info = Account.objects.get(id=request.user.id)
    lab_assignment_detail = LabAssignmentTopView.objects.get(id=id)

    session_id = lab_assignment_detail.session_id
    form = CreateLabAssignment(request.POST or None,instance=lab_assignment_detail)
    if form.is_valid():

        form.save()
        messages.success(request,"LabAssignment Has Been Updated Successfully.")
        return redirect('lab_assignment_session_view', lab_assignment_detail.group.id, session_id.batch_of.id)

    
    context = {
        'assignlabcurrent' : 'current',
        'form' : form,
        'account_info':account_info,
    }
    return render(request,'lab_assignment/edit_lab_assignment.html',context)



def lab_assignment_delete(request,id):

    lab_assignment_detail = LabAssignmentTopView.objects.get(id=id)
    lab_assignment_detail.delete()
    messages.warning(request,"LabAssignment Has Been Removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
