from django import forms
from .models import Student, Faculty, Batch, Session, Course, Teacher, Group

session_status=[('Active','active'),('Inactive','inactive')]

class EditStudentForm(forms.ModelForm):
    fathers_name = forms.CharField(label="Father's Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    mothers_name = forms.CharField(label="Mother's Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    roll_no = forms.IntegerField(label='Roll No',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    batch = forms.ModelChoiceField(label='Batch', queryset=Batch.objects.all().distinct(),widget=forms.Select(attrs={'class': 'form-control'}))     

    group = forms.ModelChoiceField(label='Group', queryset=Group.objects.all().distinct(),widget=forms.Select(attrs={'class': 'form-control'}))     
    
    class Meta:
        model = Student
        exclude = ['user']
    
    def __init__(self, *args, **kwargs):
        super(EditStudentForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['fathers_name'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['mothers_name'].widget.attrs['style']  = 'width:1000px; height:40px;'
        self.fields['roll_no'].widget.attrs['style']  = 'width:1000px; height:40px;'
        self.fields['batch'].widget.attrs['style']  = 'width:1000px; height:40px;'
        self.fields['group'].widget.attrs['style']  = 'width:1000px; height:40px;'


class EditTeacherForm(forms.ModelForm):

    
    experience = forms.IntegerField(label='Experience', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    teacher_id = forms.CharField(label='Teacher Id', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Teacher
        exclude = ['user']
    
    def __init__(self, *args, **kwargs):
        super(EditTeacherForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['experience'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['teacher_id'].widget.attrs['style']  = 'width:1000px; height:40px;'

    

class EditFacultyForm(forms.ModelForm):

    faculty_name = forms.CharField(label='Faculty Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Faculty
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditFacultyForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['faculty_name'].widget.attrs['style'] = 'width:1000px; height:40px;'
        

class EditGroupForm(forms.ModelForm):

    group_name = forms.CharField(label=' Group ', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditGroupForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['group_name'].widget.attrs['style'] = 'width:1000px; height:40px;'
        


class EditBatchForm(forms.ModelForm):

    batch_year = forms.IntegerField(label='Credit Hours',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    faculty = forms.ModelChoiceField(label='Faculty', queryset=Faculty.objects.all().distinct(),widget=forms.Select(attrs={'class': 'form-control'}))     
    group = forms.ModelMultipleChoiceField(
            queryset=Group.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )

    class Meta:
        model = Batch
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditBatchForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['batch_year'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['faculty'].widget.attrs['style'] = 'width:1000px; height:40px;'


class EditSessionForm(forms.ModelForm):

    session_id = forms.IntegerField(label='Session Id',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    semester = forms.IntegerField(label='Semester',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    batch_of = forms.ModelChoiceField(label='Batch', queryset=Batch.objects.all().distinct(),widget=forms.Select(attrs={'class': 'form-control'}))     

    active = forms.ChoiceField(choices=session_status , label='Active',widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Session
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditSessionForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['session_id'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['semester'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['batch_of'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['active'].widget.attrs['style'] = 'width:1000px; height:40px;'



class EditCourseForm(forms.ModelForm):

    course_no = forms.CharField(label=' Course No. ', widget=forms.TextInput(attrs={'class': 'form-control'}))
    course_name = forms.CharField(label=' Course Name. ', widget=forms.TextInput(attrs={'class': 'form-control'}))
    credit = forms.IntegerField(label='Credit Hours',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    faculty_id = forms.ModelChoiceField(label='Faculty', queryset=Faculty.objects.all().distinct(),widget=forms.Select(attrs={'class': 'form-control'}))     
    teacher_id = forms.ModelChoiceField(label='Teacher', queryset=Teacher.objects.all().distinct(),widget=forms.Select(attrs={'class': 'form-control'}))     
    session_id = forms.ModelChoiceField(label='Session', queryset=Session.objects.all().distinct(),widget=forms.Select(attrs={'class': 'form-control'}))     
    
    class Meta:
        model = Course
        fields = '__all__'



    def __init__(self, *args, **kwargs):
        super(EditCourseForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['course_no'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['course_name'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['credit'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['faculty_id'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['teacher_id'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['session_id'].widget.attrs['style'] = 'width:1000px; height:40px;'
        