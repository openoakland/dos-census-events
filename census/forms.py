from django.forms import ModelForm
from django  import forms
from datetime import datetime
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'organization_name',
            'location',
            'event_type',
            'is_census_equipped',
            'languages',
            'start_datetime',
            'end_datetime',
            'recurrences',
            'contact_name',
            'contact_email',
            'contact_phone',
        ]
        widgets = {
                'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime'}),
                'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime'})
        }
