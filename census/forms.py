from django.forms import ModelForm, Widget
from django  import forms
from datetime import datetime
from .models import Event

class UswdsTextInput(Widget):
    def get_context(self, name, value, attrs):
        context = super(Widget, self).get_context(name, value, attrs)
        context['template_name'] = 'includes/forms/text_input.html'
        return context


class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
                'start_time': forms.TimeInput(attrs={'type': 'time'}),
                'end_time': forms.TimeInput(attrs={'type': 'time'}),
                'title': UswdsTextInput(attrs={'class': 'usa-input'}),
                'description': forms.TextInput(attrs={'class': 'usa-input'}),
                'organization_name': forms.TextInput(attrs={'class': 'usa-input'}),
                'event_type': forms.TextInput(attrs={'class': 'usa-select'}),
                'location': forms.TextInput(attrs={'class': 'usa-input'}),
                'is_census_equipped': forms.TextInput(attrs={'class': 'usa-checkbox'}),

        }
        exclude = ['approval_status', 'lon', 'lat']

