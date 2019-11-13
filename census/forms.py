from django.forms import ModelForm
from django  import forms
from datetime import datetime
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
                'start_time': forms.TimeInput(attrs={'type': 'time'}),
                'end_time': forms.TimeInput(attrs={'type': 'time'})
        }
        exclude = ['approval_status', 'lon', 'lat'
                #temporarily don't include these till the template is ready
                , 'contact_name', 'contact_email', 'contact_phone', 'languages'
                ]
