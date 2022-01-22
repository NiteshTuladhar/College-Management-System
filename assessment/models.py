from django.db import models
from student.models import Course, Student, Session
from teacher.models import Teacher
from django.core.validators import MinValueValidator, MaxValueValidator

from InternalMarksPrediction.models import InternalMaks
from django.db.models.signals import post_save

# Create your models here.
assesmentType = [('Class Test','Class Test'), ('Mid-Term','Mid-Term'),('Final-Term','Final-Term')]

class AssessmentTopView(models.Model):
    assessment_type = models.CharField(max_length=50, choices=assesmentType)
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete = models.CASCADE)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)


class Assesment(models.Model):
    assesment_name = models.ForeignKey('AssessmentTopView', on_delete = models.CASCADE)
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(101)])


    def __str__(self):

    	return self.student_name.user.full_name






def AssesmentSignal(sender, **kwargs):

    updated_student_info = kwargs['instance']

    student_id = updated_student_info.student_name.id
    student_course = updated_student_info.assesment_name.course_name.id



    #CLASS TEST
    try:
        class_assesment = AssessmentTopView.objects.get(course_name_id = student_course, assessment_type = 'Class Test')
        class_assesment_marks = Assesment.objects.get(assesment_name = class_assesment, student_name_id= student_id) 
        class_assessment_marks = class_assesment_marks.marks
    
    except:
        class_assessment_marks= 0



    #MID TERM
    try:
        mid_assesment = AssessmentTopView.objects.get(course_name_id = student_course, assessment_type = 'Mid-Term')
        mid_assessment_marks = Assesment.objects.get(assesment_name = mid_assesment, student_name_id= student_id) 
        mid_assessment_marks = mid_assessment_marks.marks

    except:

        mid_assessment_marks= 0



    #FINAL TERM
    
    try:
        final_assesment = AssessmentTopView.objects.get(course_name_id = student_course, assessment_type = 'Final-Term')
        final_assessment_marks = Assesment.objects.get(assesment_name = final_assesment, student_name_id= student_id) 
        final_assessment_marks = final_assessment_marks.marks
    except:
        final_assessment_marks= 0


    #Assessment
    #Class-Assessment
    internal_class_assessment = (class_assessment_marks/20)*1

    #Mid-Term Assessment
    internal_mid_assessment = mid_assessment_marks
    if internal_mid_assessment>80:
        internal_mid_assessment=4
    elif internal_mid_assessment>60:
        internal_mid_assessment = 3
    elif internal_mid_assessment>40:
        internal_mid_assessment = 2
    else:
        internal_mid_assessment = 0

    #Final-Term Assessment
    internal_final_assessment = final_assessment_marks
    if internal_final_assessment>80:
        internal_final_assessment=7
    elif internal_final_assessment>60:
        internal_final_assessment = 6
    elif internal_final_assessment>40:
        internal_final_assessment = 4
    else:
        internal_final_assessment = 0


    ultimate_assesment_marks = internal_class_assessment + internal_mid_assessment + internal_final_assessment

    student_internal_marks, created = InternalMaks.objects.get_or_create(student_id = student_id, course_id = student_course)

    
    student_internal_marks.assesment_marks = ultimate_assesment_marks
    student_internal_marks.save()

post_save.connect(AssesmentSignal,sender=Assesment)