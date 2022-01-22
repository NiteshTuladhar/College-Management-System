from django.db import models

# Create your models here.
from django.db import models
from student.models import Student, Session, Course, Group
from teacher.models import Teacher
from InternalMarksPrediction.models import InternalMaks
from django.db.models.signals import post_save
# Create your models here.

class AssignmentTopView(models.Model):
    question = models.TextField()
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    deadline = models.DateField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return f'Assigment Course of {self.course_id} by {self.teacher_id} on {self.session_id}'

check = [('Submitted', 'Submitted'), ('Not Submitted', 'Not Submitted')]
    

class Assignment(models.Model):
    assignment_name = models.ForeignKey('AssignmentTopView', on_delete=models.CASCADE, null=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment_file = models.FileField(upload_to='subitted_assignments',blank=True,null=True)
    submitted_on = models.DateField(null=True)
    submitted = models.CharField(max_length=30, choices=check, default=check[1])

    def __str__(self):
        return f'Assigment of {self.student_id} is {self.submitted}'



class LabAssignmentTopView(models.Model):
    question = models.TextField()
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    deadline = models.DateField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'Lab Assigment Course of {self.course_id} by {self.teacher_id} on {self.session_id}'

check = [('Submitted', 'Submitted'), ('Not Submitted', 'Not Submitted')]


    
class LabAssignment(models.Model):
    assignment_name = models.ForeignKey('LabAssignmentTopView', on_delete=models.CASCADE, null=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    lab_assignment_file = models.FileField(upload_to='subitted_lab_assignments',blank=True,null=True)
    submitted_on = models.DateField(null=True)
    submitted = models.CharField(max_length=30, choices=check, default=check[1])

    def __str__(self):
        return f'Lab Assigment of {self.student_id} is {self.submitted}'





def AssignmentSignal(sender, **kwargs):

    updated_student_info = kwargs['instance']

    student_id = updated_student_info.student_id.id
    student_course = updated_student_info.assignment_name.course_id.id


    assignment = AssignmentTopView.objects.filter(course_id_id=student_course)
    assignment_submitted = Assignment.objects.filter(assignment_name__in=assignment, student_id_id=student_id, submitted='Submitted').count()
    assignment_not_submitted = Assignment.objects.filter(assignment_name__in=assignment, student_id_id=student_id, submitted='Not Submitted').count()
    total_assignment = AssignmentTopView.objects.filter(course_id_id=student_course).count()


    internal_class_assignment = (assignment_submitted/total_assignment)*10
    

    student_internal_marks, created = InternalMaks.objects.get_or_create(student_id = student_id, course_id = student_course)
    
    student_internal_marks.assignment_marks = internal_class_assignment
    student_internal_marks.save()
    
    print('try chalyto')
   
    

post_save.connect(AssignmentSignal,sender=Assignment)



def LabAssignmentSignal(sender, **kwargs):

    updated_student_info = kwargs['instance']

    student_id = updated_student_info.student_id.id
    student_course = updated_student_info.assignment_name.course_id.id


    lab_assignment = LabAssignmentTopView.objects.filter(course_id_id=student_course)
    lab_assignment_submitted = LabAssignment.objects.filter(assignment_name__in=lab_assignment, student_id_id=student_id, submitted='Submitted').count()
    lab_assignment_not_submitted = LabAssignment.objects.filter(assignment_name__in=lab_assignment, student_id_id=student_id, submitted='Not Submitted').count()
    total_lab_assignment = LabAssignmentTopView.objects.filter(course_id_id=student_course).count()


    internal_class_lab_assignment = (lab_assignment_submitted/total_lab_assignment)*10

    student_internal_marks, created = InternalMaks.objects.get_or_create(student_id = student_id, course_id = student_course)

    
    
    
    student_internal_marks.lab_assignment_marks = internal_class_lab_assignment
    student_internal_marks.save()

post_save.connect(LabAssignmentSignal,sender=LabAssignment)