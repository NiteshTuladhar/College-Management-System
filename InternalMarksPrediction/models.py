from django.db import models
from student.models import *
from django.db.models.signals import post_save
import _datetime




class InternalMaks(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True)
    lab_assignment_marks = models.FloatField(default=0,blank=True, null=True)
    assignment_marks = models.FloatField(default=0,blank=True, null=True)
    attendance_marks = models.FloatField(default=0,blank=True, null=True)
    lab_attendance_marks = models.FloatField(default=0,blank=True, null=True)
    assesment_marks = models.FloatField(default=0,blank=True, null=True)
    total_internal_marks = models.FloatField(default=0,blank=True, null=True)
    def __str__(self):

        return self.student.user.full_name

    @property
    def calculateInternalMarks(self):

        total_assesment_marks = self.assesment_marks
        internal_attendance = self.attendance_marks
        internal_lab_attendance = self.lab_attendance_marks
        total_assignment_marks = ((self.assignment_marks+self.lab_assignment_marks)/20)*3

        internal_class_activity = float((self.assignment_marks + self.lab_assignment_marks + self.lab_attendance_marks + self.attendance_marks)/23)*3


        internal_marks =  total_assesment_marks + internal_attendance + internal_lab_attendance + total_assignment_marks + internal_class_activity

        self.total_internal_marks = internal_marks

        return internal_marks





class WeeklyInternalMaks(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True)
    daily_internal_marks = models.FloatField(default=0,blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    week_created = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):

        return self.student.user.full_name




def calculateInternalMarks(sender, **kwargs):

    updated_student_info = kwargs['instance']
    student_id = updated_student_info.student.id
    student_course = updated_student_info.course.id

    internalmarks = InternalMaks.objects.get(student_id=student_id,course=student_course)

    total_assesment_marks = internalmarks.assesment_marks
    internal_attendance = internalmarks.attendance_marks
    internal_lab_attendance = internalmarks.lab_attendance_marks
    total_assignment_marks = ((internalmarks.assignment_marks+internalmarks.lab_assignment_marks)/20)*3

    internal_class_activity = float((internalmarks.assignment_marks+internalmarks.lab_assignment_marks+internalmarks.lab_attendance_marks+internalmarks.attendance_marks)/23)*3


    internal_marks =  total_assesment_marks + internal_attendance + internal_lab_attendance + total_assignment_marks + internal_class_activity

    internalmarks.total_internal_marks = internal_marks
    
    #For weekly internal marks
    week = _datetime.date.today().isocalendar()[1]
    try:
        weekly_internal_marks = WeeklyInternalMaks.objects.get(student_id=student_id,course_id=student_course, week_created=week)
        weekly_internal_marks.daily_internal_marks = internal_marks
        weekly_internal_marks.save()
    except:
        daily_internal_marks = WeeklyInternalMaks.objects.create(student_id=student_id,course_id=student_course,daily_internal_marks=internal_marks,week_created=week)
    
    print('----------SIGNAL INTERNAL MARKS OF STUDENT-----------------')
    print(internalmarks.total_internal_marks)

    
    #internalmarks.save()

class TotalMarks(models.Model):
    
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_assignment_marks = models.PositiveBigIntegerField(default=0)
    total_lab_assignment_marks = models.PositiveBigIntegerField(default=0)
    total_attendance_marks = models.PositiveBigIntegerField(default=0)
    total_lab_attendance_marks = models.PositiveBigIntegerField(default=0)
    total_class_assesment_marks = models.PositiveBigIntegerField(default=0)
    total_mid_assessment_marks = models.PositiveBigIntegerField(default=0)
    total_final_assessment_marks = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return str(self.user)


post_save.connect(calculateInternalMarks,sender=InternalMaks)



