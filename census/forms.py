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
            'lat',
            'lon',
            'start_datetime',
            'end_datetime',
            'recurrences',
            'contact_name',
            'contact_email',
            'contact_phone',
            'is_private_event'
        ]
        widgets = {
                'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime'}),
                'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime'})
        }

class EditEventForm(ModelForm):
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
            'lat',
            'lon',
            'start_datetime',
            'end_datetime',
            'recurrences',
            'contact_name',
            'contact_email',
            'contact_phone',
            'approval_status',
            'is_private_event'
        ]
        widgets = {
                'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime'}),
                'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime'})
        }
