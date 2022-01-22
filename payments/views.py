from django.shortcuts import render, redirect
from payments.models import Payment, PaymentInfo
from student.models import * 
from .form import CreatePaymentInfo
import datetime
import requests 
from .token import generatetoken
from django.http import JsonResponse
from django.contrib import messages

def createPaymentInfo(request):

    account_info = request.user
    
    form = CreatePaymentInfo()
    
    if request.method == 'POST':
        form = CreatePaymentInfo(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)

            amount = request.POST['amount']
            payment_name = request.POST['payment_name']
            semester = request.POST['semester']

            session = Session.objects.get(id = semester)

            paymentinfo = PaymentInfo.objects.create(semester=session, payment_name=payment_name, amount=amount)
            
            
            batch = session.batch_of
            list_students = Student.objects.filter(batch=batch)


            for l in list_students:
                make_payment, created = Payment.objects.get_or_create(payment_of_id = paymentinfo.id, student=l
                                    ,payment_amount = paymentinfo.amount,payment_due=paymentinfo.amount)

            return redirect('listpayment')

    context = {
        'account_info' : account_info,
        'billcurrent' : 'current',
        'form' : form,

    }

    return render(request, 'payment/add_new_paymentinfo.html',context)
     

def listPaymentInfo(request):

    account_info = request.user    
    payments = PaymentInfo.objects.all().order_by('-date_created')

    context ={
        'account_info' : account_info,
        'billcurrent' : 'current',  
        'payments' : payments
    }

    return render(request, 'payment/list_payment_info.html',context)


def payments(request):

    account_info = request.user
    student = Student.objects.get(user=request.user)
    batch = student.batch
    session = Session.objects.get(batch_of = batch)
    my_payments_info = PaymentInfo.objects.filter(semester = session)
    my_payments = Payment.objects.filter(payment_of__in=my_payments_info, student=student, full_payment=False)

    

    context = {
        'account_info' : account_info,
        'billcurrent' : 'current',
        'my_payments' : my_payments,
        
    }

    return render(request,'payment/payment.html', context)



def makePayment(request,id):
    
    account_info = request.user
    student = Student.objects.get(user=request.user)
    inpayment = Payment.objects.get(id=id)
    pid = inpayment.payment_of.id
    payment = PaymentInfo.objects.get(id = pid)

    make_payment, created = Payment.objects.get_or_create(payment_of_id = payment.id, student=student
                                    ,payment_amount = payment.amount)




    context = {
        'account_info' : account_info,
        'make_payment' : make_payment
    }
    return render(request,'payment/payment_form.html',context)


def getAmount(request, id):

    payment_info = Payment.objects.get(id=id)
  

    if request.method == 'POST':
        amount = request.POST.get('amount')

        payment_info.transaction_id = generatetoken()
        payment_info.save()


    context = {
        'amount' : amount,
        'payment_info' : payment_info
    }
    return render(request,'payment/esewa.html',context)



def esewa(request, id):
    if request.method == 'GET':
        totalAmt = request.GET['amt']
        oid = request.GET.get('oid')
        refid = request.GET['refId']

        payment = Payment.objects.get(id=id)
        print(payment)
        print('---------------level 1-------------------') 

        import xml.etree.ElementTree as ET

        url ="https://uat.esewa.com.np/epay/transrec"
        d = {
        'amt': totalAmt,
        'scd': 'EPAYTEST',
        'rid': refid,
        'pid': oid,
 
        }


        resp = requests.post(url,d)
        root = ET.fromstring(resp.content)
        status = root[0].text.strip()


        if status == "Success":

            total_amount = payment.payment_due
            payment.payment_due = total_amount - int(float(totalAmt))
            payment.payment_id = datetime.datetime.now().timestamp()

            if payment.payment_due <= 0:
                payment.full_payment = True
                messages.success(request,"Your Full payment has been done")
            else:
                messages.success(request,"Your Partial payment has been done")
            payment.save()
            
    return redirect('payment')



def payment_edit(request, id):
    account_info = Account.objects.get(id=request.user.id)
    payment = PaymentInfo.objects.get(id=id)
    form = CreatePaymentInfo(request.POST or None, instance=payment)
    print(form)
    if form.is_valid():
        print('=====================done============================')
        form = form.save()
        messages.success(request,"Your Payment has been successfully edited")
        return redirect('listpayment')

    
    context = {
        'payment': payment,
        'billcurrent' : 'current', 
        'form' : form,
        'account_info':account_info,
    }

    return render(request,'payment/edit_payment.html',context)


def payment_delete(request, id):
    payment = PaymentInfo.objects.get(id=id)
    payment.delete()
    messages.warning(request,"Payment Has Been Deleted.")
    return redirect('listpayment')

	