from django.db import models
from student.models import Student
# Create your models here.

class ContactUs(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    text = models.TextField()
    checked = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)
    reply = models.TextField(null=True, blank=True)
