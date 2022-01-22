from django import forms
from .models import Assignment, AssignmentTopView, LabAssignment, LabAssignmentTopView

class CreateAssignment(forms.ModelForm):

    class Meta:
        model = AssignmentTopView
        fields = ('question','description','deadline')


class CreateLabAssignment(forms.ModelForm):

    class Meta:
        model = LabAssignmentTopView
        fields = ('question','deadline')