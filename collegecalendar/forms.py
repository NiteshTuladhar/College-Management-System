from django.forms import ModelForm, DateInput
from collegecalendar.models import Event, EventMember
from django import forms

class EventForm(ModelForm):

  title = forms.CharField(label='Event Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
  description = forms.CharField(label='Event Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
  start_time =  forms.DateField(label='Event Start Date', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
  end_time = forms.DateField(label='Event End Date', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

  class Meta:
    model = Event
    exclude = ['user']

     

class AddMemberForm(forms.ModelForm):
  class Meta:
    model = EventMember
    fields = ['session']

  def __init__(self, *args, **kwargs):
      super(AddMemberForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
      self.fields['session'].widget.attrs['style'] = 'width:400px; height:40px;background-color:white;'
      