from django import forms
from .models import PaymentInfo
from student.models import Session

class CreatePaymentInfo(forms.ModelForm):
    
    semester = forms.ModelChoiceField(label='Semester', queryset=Session.objects.all().distinct(),widget=forms.Select(attrs={'class': 'form-control'}))     
    payment_name = forms.CharField(label='Payment Name or Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
    amount = forms.CharField(label='Amount', widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = PaymentInfo

        fields = ['semester','payment_name','amount']


    def __init__(self, *args, **kwargs):
        super(CreatePaymentInfo, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['semester'].widget.attrs['style'] = 'width:1000px; height:40px;'
        self.fields['payment_name'].widget.attrs['style']  = 'width:1000px; height:200px;'
        self.fields['amount'].widget.attrs['style']  = 'width:1000px; height:40px;'
        
        
