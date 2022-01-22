from django.db import models
from datetime import datetime, timezone
from student.models import Session, Student
payment_methods = [
   ("ESEWA","ESEWA")
]

payment_methods = [
   ("ESEWA","ESEWA")
]
# Create your models here.

class PaymentInfo(models.Model):
    
    semester = models.ForeignKey(Session, on_delete=models.CASCADE)
    payment_name = models.CharField(max_length=50, null=True,blank=True)
    amount = models.DecimalField(decimal_places=3, max_digits=10)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):

        return self.payment_name



class Payment(models.Model):

    payment_of = models.ForeignKey('PaymentInfo', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=50, null=True, blank=True)
    transaction_id = models.CharField(max_length=50,null=True,blank=True)
    payment_amount = models.DecimalField(decimal_places=3, max_digits=10)
    full_payment = models.BooleanField(default=False)
    payment_due = models.DecimalField(decimal_places=3, max_digits=10, null=True,blank=True)
    paid_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):

        return self.payment_of.payment_name



    






