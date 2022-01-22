from django import forms
from .models import Account,gender_list

status=[('Yes','yes'),('No','no')]

class Add_New_User(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(label='Date Of Birth', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(label='Gender', widget=forms.Select(attrs={'class': 'form-control'}), choices=gender_list)
    address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_no = forms.IntegerField(label='Contact Number',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Account
        exclude = ['image', 'last_login', 'password', 'is_first_login']

    
    def __init__(self, *args, **kwargs):
        super(Add_New_User, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['email'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['date_of_birth'].widget.attrs['style']  = 'width:1000px; height:40px;'
        self.fields['gender'].widget.attrs['style']  = 'width:1000px; height:40px;'
        self.fields['address'].widget.attrs['style']  = 'width:1000px; height:40px;'
        self.fields['full_name'].widget.attrs['style']  = 'width:1000px; height:40px;'
        self.fields['contact_no'].widget.attrs['style']  = 'width:1000px; height:40px;'
        

