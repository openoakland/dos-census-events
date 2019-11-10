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
            if visible.name in ['title', 'event_type', 'location', 'organization_name']:
                visible.field.widget.attrs['class'] = 'usa-input'
            elif visible.name in ['description']:
                visible.field.widget.attrs['class'] = 'usa-textarea'