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
            'event_type',
            'is_census_equipped',
            'languages',
            'lat',
            'lon',
            'site_name',
            'location',
            'city',
            'zip_code',
            'start_datetime',
            'end_datetime',
            'recurrences',
            'contact_name',
            'contact_email',
            'contact_phone',
            'is_private_event',
            'is_ada_compliant',
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
            'event_type',
            'is_census_equipped',
            'languages',
            'lat',
            'lon',
            'site_name',
            'location',
            'city',
            'zip_code',
            'start_datetime',
            'end_datetime',
            'recurrences',
            'contact_name',
            'contact_email',
            'contact_phone',
            'approval_status',
            'is_private_event',
            'is_ada_compliant',
        ]
        widgets = {
                'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime'}),
                'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime'})
        }
