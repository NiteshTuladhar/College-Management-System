from django import forms
from .models import NoticeBoard
from student.models import Session, Course

class FormNoticeBoard(forms.ModelForm):
    notice_title = forms.CharField(label='Notice Title',widget=forms.TextInput(attrs={'class': 'form-control', }))
    notice_description = forms.CharField(label='Notice Description', widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 0, 'rows': 20}))
    semester = forms.ModelChoiceField(queryset=Session.objects.all(), label = 'For Semester', widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = NoticeBoard
        exclude = ['notice_date','notice_annoucer', 'type' ]


