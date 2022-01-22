from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from student.models import *
from teacher.models import *
from .forms import CreateAssessment, AssessmentView
from django.contrib import messages
# Create your views here.

def assesment_home(request):
    teacher = Teacher.objects.get(user_id = request.user.id)
    faculty = Faculty.objects.all()        
    course = Course.objects.filter(teacher_id_id=teacher)
    account_info = Account.objects.get(id=request.user.id)

    context = {
        'asseslabcurrent' : 'current',
        'course': course,
        'account_info' : account_info,
        'faculty': faculty
    }

    return render(request,'assessment/assessment.html', context)


def assessment_batch(request, id):
    batch = Batch.objects.filter(faculty_id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    account_info = Account.objects.get(id=request.user.id)

    context = {
        'asseslabcurrent' : 'current',
        'batch': batch,
        'teacher': teacher,
        'account_info' : account_info
    }

    return render(request, 'assessment/assessment_batch_view.html', context)



def assessment_session_view(request, id):
    context = {}

    account_info = Account.objects.get(id=request.user.id)
    session = Session.objects.get(batch_of_id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.filter(session_id_id=session.id, teacher_id=teacher)
    course_length = len(course)
    if course_length==0:
        return redirect('errorpage')
    else:
        student = Student.objects.filter(batch_id = id)
        assesment = AssessmentTopView.objects.filter(teacher_name=teacher, course_name__in=course, session=session)
        context.update({'assessment': assesment,'session':session, 'course': course,'asseslabcurrent' : 'current'})
    context.update({'account_info':account_info})

    return render(request, 'assessment/assessment_session_view.html', context)


def create_assessment(request, id):

    account_info = Account.objects.get(id=request.user.id)
    student = Student.objects.filter(batch_id=id)
    session = Session.objects.get(batch_of_id=id)
    teacher = Teacher.objects.get(user_id=request.user.id)
    course = Course.objects.get(session_id_id=session.id, teacher_id=teacher)
    try:
        form = CreateAssessment()
        if request.method == "POST":
            form = CreateAssessment(request.POST or None)
            if form.is_valid():
                form = form.save(commit=False)
                form.teacher_name = teacher
                form.course_name = course
                form.session = session
                form.save()
                messages.success(request,"Assesment Has Been Checked.")

                assessment_detail = AssessmentTopView.objects.get(id=form.id)
                for s in student:
                    checks = Assesment(student_name_id=s.id, assesment_name=assessment_detail, marks=0)
                    checks.save()
                return redirect('assessment_session_view', session.batch_of.id)
    except:
        print('ok-------------------------------------------------------')

    context = {
        'asseslabcurrent' : 'current',
        'course': course,
        'form': form,
        'account_info' : account_info
    }
    return render(request,'assessment/create_assessment.html', context)


def assessment_check_view(request, id):
    context = {}
    account_info = Account.objects.get(id=request.user.id)
    assessment_detail = AssessmentTopView.objects.get(id=id)
    
    
    assessment_id = assessment_detail.id
    
    sid = assessment_detail.session
    
    batch = sid.batch_of
    
    students = Student.objects.filter(batch=batch)
    marks = Assesment.objects.filter(assesment_name_id=assessment_id, student_name__in=students)
   

    context.update({

        'asseslabcurrent' : 'current',
        'ass':assessment_detail,
        'students': students,
        'ids':assessment_id,
        'marks' : marks,
        'account_info' : account_info,
        'batch' : batch,

    })
    return render(request,'assessment/check_assessment.html', context)



def assessment_edit(request,id):

    account_info = Account.objects.get(id=request.user.id)
    assesment_detail = AssessmentTopView.objects.get(id=id)

    session_id = assesment_detail.session_id
    print(assesment_detail)

    form = CreateAssessment(request.POST or None,instance=assesment_detail)
    if form.is_valid():

        form.save()
        messages.success(request,"Assesment Has Been Updated Successfully.")
        return redirect('assessment_session_view', session_id)

    
    context = {
        'asseslabcurrent' : 'current',
        'form' : form,
        'account_info':account_info,
    }
    return render(request,'assessment/edit_assessment.html',context)



def getmarks(request, id, sid):
    context = {}
    account_info = Account.objects.get(id=request.user.id)
    assessment_detail = AssessmentTopView.objects.get(id=id)
    
    
    assessment_id = assessment_detail.id
    print(assessment_id)
    print(sid)
    students = Student.objects.get(id=sid)
  

    if request.method == 'GET':
        arks = request.GET.get('mark')
        print(arks)
        marks = int(arks)
        print(type(marks))

        if (assessment_detail.assessment_type == 'Class Test' ):

            if(marks >=0 and marks<=20 ):

                print('Class Test')
                work = Assesment.objects.get(assesment_name=assessment_detail, student_name=students)
                work.marks = marks
                work.save()

        elif (assessment_detail.assessment_type == 'Mid-Term' or assessment_detail.assessment_type == 'Final-Term' ):

            print('TTTTTTTTTTTTTTTTHHHHHHHHIIIICCCCCCCCCC XAAAAAAAAAAAAAAAAA')
            if(marks >=0 and marks<=100):
                print('Final and mid term')
                work = Assesment.objects.get(assesment_name=assessment_detail, student_name=students)
                work.marks = marks
                work.save()

    context.update({
        'asseslabcurrent' : 'current',
        'ass':assessment_detail,
        'students': students,
        'ids':assessment_id,
        'account_info' : account_info,

      

    })
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def assesment_delete(request,id):

    assessment = AssessmentTopView.objects.get(id=id)
    assessment.delete()
    messages.warning(request,"Assesment Has Been Deleted.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def errorpage(request):

    return render(request,'error_folder/error_display.html')


    
def errorpage(request):

    return render(request,'error_folder/error_display.html')



def return_back(request,id):    

    session_id = Session
    return redirect('assessment_session_view', session_id)