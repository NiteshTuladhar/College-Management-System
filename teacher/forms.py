from django import forms
from .models import Teacher

class Edit_Teacher_Form(forms.ModelForm):

    experience = forms.IntegerField(label='Experience',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    teacher_id = forms.CharField(label="Teacher's Id", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Teacher
        exclude = ['user']

    
    def __init__(self, *args, **kwargs):
        super(Edit_Teacher_Form, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['experience'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['teacher_id'].widget.attrs['style']  = 'width:1000px; height:40px;'
        