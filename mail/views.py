from django.shortcuts import render,redirect
from .models import ContactUs
from .form import ContactForm
from student.models import Student
from django.contrib import messages
# Create your views here.

def contactus(request):
    form = ContactForm()
    user = Student.objects.get(user_id=request.user.id)
    if request.method == "POST":
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.save()
            messages.success(request,"Your Application Has Been Submitted")
            return redirect('student_dashboard')
    context = {
        'contactcurrent' : 'current',
        'form': form,
        'account_info': request.user,

    }

    return render(request, 'contactus/contactus.html', context)


def viewmail(request):

    mail = ContactUs.objects.all().order_by('-date')
    for m in mail:
        m.checked = True
        m.save()

    context={
        'mail': mail,
        'account_info': request.user,

    }

    return render(request,'contactus/viewmail.html', context)




def viewmailStudent(request):

    user = Student.objects.get(user_id = request.user.id)
    mail = ContactUs.objects.filter(user=user).order_by('-date')
    for m in mail:
        m.checked = True
        m.save()

    context={
        'mail': mail,
        'account_info': request.user,

    }

    return render(request,'contactus/viewmail_student.html', context)


def replyMail(request,id):

    mail = ContactUs.objects.get(id=id)

    context = {
        'mail' : mail
    }
    return render(request,'contactus/reply.html',context)


def saveReply(request,id):

    mail = ContactUs.objects.get(id=id)
    if request.method == 'POST':

        reply = request.POST['reply']

        print(reply)
        mail.reply = reply
        mail.save()

    return redirect('view_contactus')