from InternalMarksPrediction.models import InternalMaks
from student.models import Student

from django.shortcuts import render, get_object_or_404

#----IMPORTS FOR PDF GENERATION--#

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def student_report_render_pdf_view(request,id,*args, **kwargs):
    
    pk = kwargs.get('id')
    

    student = Student.objects.get(user_id=id)
    intmarks = InternalMaks.objects.filter(student=student)

    total_marks = 0
    credit = 0
    for i in intmarks:

        total_marks += i.calculateInternalMarks
        credit += i.course.credit 

    template_path = 'pdf/pdf2.html'
    context = {
        
        'intmarks': intmarks ,
        'total_marks' : total_marks,
        'credit' : credit
        
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    #if download:
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #if view:
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



