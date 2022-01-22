from django import forms
from .models import AssessmentTopView, Assesment

class CreateAssessment(forms.ModelForm):

    class Meta:
        model = AssessmentTopView
        fields = ('assessment_type','start_date','end_date')



class AssessmentView(forms.ModelForm):

    class Meta:
        model = Assesment
        fields = ('marks',)
    

