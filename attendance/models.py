from django.db import models
from student.models import *
from teacher.models import Teacher
from django.db.models.signals import post_save
from InternalMarksPrediction.models import InternalMaks
# Create your models here.

class Attendance(models.Model):
    date = models.DateField(auto_now=True)
    course_of = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.date} || {self.student_id.roll_no}   ||     {self.student_id.user}  || {self.status}'

class PermissionAttendance(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Lab_Attendance(models.Model):
    date = models.DateField(auto_now=True)
    course_of = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)


    def __str__(self):
        return f' (Lab) {self.date} || {self.student_id.roll_no}   ||     {self.student_id.user}  || {self.status}'



def AttendanceSignal(sender, **kwargs):

    updated_student_info = kwargs['instance']

    student_id = updated_student_info.student_id.id
    student_course = updated_student_info.course_of.id


    
    total_attendance = Attendance.objects.filter(course_of_id=student_course, student_id_id = student_id).count()
    attendance_present = Attendance.objects.filter(course_of_id=student_course, student_id_id = student_id, status=True).count()
    attendance_absent = Attendance.objects.filter(course_of_id=student_course, student_id_id = student_id, status=False).count()


    internal_attendance = (attendance_present/total_attendance) * 1.5

    print('---------total present-------------')
    print(attendance_present)
    print('---------total absent-------------')
    print(attendance_absent)
    print('internal atendance')
    print(internal_attendance)


    student_internal_marks, created = InternalMaks.objects.get_or_create(student_id = student_id, course_id = student_course)
    student_internal_marks.attendance_marks = internal_attendance
    student_internal_marks.save()

post_save.connect(AttendanceSignal,sender=Attendance)




def LabAttendanceSignal(sender, **kwargs):

    updated_student_info = kwargs['instance']

    student_id = updated_student_info.student_id.id
    student_course = updated_student_info.course_of.id


    
    total_Labattendance = Lab_Attendance.objects.filter(course_of_id=student_course, student_id_id = student_id).count()
    labattendance_present = Lab_Attendance.objects.filter(course_of_id=student_course, student_id_id = student_id, status=True).count()
    labattendance_absent = Lab_Attendance.objects.filter(course_of_id=student_course, student_id_id = student_id, status=False).count()


    internal_labattendance = (labattendance_present/total_Labattendance) * 1.5

    print('---------total present-------------')
    print(labattendance_present)
    print('---------total absent-------------')
    print(labattendance_absent)
    print('internal atendance')
    print(internal_labattendance)


    student_internal_marks, created = InternalMaks.objects.get_or_create(student_id = student_id, course_id = student_course)
    student_internal_marks.lab_attendance_marks = internal_labattendance
    student_internal_marks.save()

post_save.connect(LabAttendanceSignal,sender=Lab_Attendance)