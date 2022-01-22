from django.db import models
from Accounts.models import Account
from teacher.models import Teacher

gender_status=[('Male','male'),('Female','female'),('Other','other')]
session_status=[('Active','active'),('Inactive','inactive')]
# Create your models here.

class Group(models.Model):
    group_name = models.CharField(max_length=10, null=True,blank=True)

    def __str__(self):
        return self.group_name

class Student(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    fathers_name = models.CharField(max_length=50)
    mothers_name = models.CharField(max_length=50)
    roll_no = models.PositiveIntegerField(default=0)
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE,blank=True,null=True)


    def __str__(self):
        return f'{self.user} of {self.batch} Batch'



class Batch(models.Model):

    batch_year = models.IntegerField()
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    group = models.ManyToManyField('Group')

    def __str__(self):
        return f'{self.batch_year}||({self.faculty})'


    

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=20)
    def __str__(self):
        return self.faculty_name


class Course(models.Model):
    course_no = models.CharField(max_length=10)
    course_name = models.CharField(max_length=20)
    credit = models.PositiveIntegerField(null=True,blank=True)
    faculty_id = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.ForeignKey('Session', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'{self.course_name}'


class Session(models.Model):
    session_id = models.IntegerField(unique=True)
    semester = models.IntegerField()
    batch_of = models.ForeignKey('Batch', on_delete=models.CASCADE)
    active = models.CharField(max_length=30, choices=session_status,null=True, blank=True)
    def __str__(self):
        return f'Semester of {self.semester} of {self.batch_of} Batch'



class CourseColor(models.Model):

    course = models.ForeignKey('Course',on_delete=models.CASCADE)
    color_code = models.CharField(max_length=10)

    def __str__(self):

        return self.course.course_name