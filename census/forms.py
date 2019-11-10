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
        exclude = ['approval_status', 'lon', 'lat']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # if visible.name in ['title', 'description', 'event_type', 'location', 'approval_status']:
            #     visible.field.widget.attrs['class'] = 'usa-input'
            # else:
            #     visible.field.widget.attrs['class'] = 'usa-input'
            visible.field.widget.attrs['class'] = 'usa-input'