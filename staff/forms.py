from django import forms
from .models import Staff

class Edit_form_staff(forms.ModelForm):

    class Meta:
        model = Staff
        fields = '__all__'