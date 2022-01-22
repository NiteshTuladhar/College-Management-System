from django import forms
from .models import ContactUs

class ContactForm(forms.ModelForm):
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 0, 'rows': 15}))


    class Meta:
        model = ContactUs
        exclude = ['user','checked','reply']