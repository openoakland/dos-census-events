from django.db import models
from recurrence.fields import RecurrenceField
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField

from . import constants

#class EventManager(models.Manager):
#    def get_queryset(self):
#        '''
#        Filter out pending events by default. If you need pending and active,
#        use Event.with_pending instead of Event.objects.
#        '''
#        return super(EventManager, self).get_queryset().filter(approval_status=constants.EventApprovalStatus.APPROVED)


class Event(models.Model):
    title = models.CharField(max_length=100, help_text="Title or short description of the event")
    description = models.TextField(blank=True, help_text="Full description of the event")
    recurrences = RecurrenceField(default=None, blank=True, help_text="This event occurs more than once.")
    start_datetime = models.DateTimeField(help_text="When does the event start?")
    end_datetime = models.DateTimeField(help_text="When does the event end?")
    organization_name = models.CharField(max_length=100, help_text="Name of the hosting organization")
    event_type = models.CharField(max_length=20, choices=[(t.name, t.value) for t in constants.EventType])
    location = models.CharField(max_length=100, help_text="Location where the event will take place")
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default=None)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default=None)
    is_census_equipped = models.BooleanField(default=False, help_text="Is this event technologically equipped to allow people to take the census?")
    approval_status = models.CharField(max_length=20, default=constants.EventApprovalStatus.PENDING.name, choices=[(t.name, t.value) for t in constants.EventApprovalStatus])
    languages = MultiSelectField(choices=[(t.name, t.value) for t in constants.Languages], help_text="Add languages supported at the event")
    contact_name = models.CharField(max_length=100, null=True, help_text="Name of contact for event")
    contact_email = models.EmailField(max_length=60, null=True, help_text="Email for contact")
    contact_phone = PhoneNumberField(null=True, help_text="Phone number for contact")

    # If you need pending and active, use Event.with_pending instead of Event.objects
    #with_pending = models.Manager()

    def __str__(self):
        return self.title


class GoogleEvent(models.Model):
    google_calendar_id = models.CharField(max_length=100)
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='google_event')
    published = models.DateTimeField(help_text="Time when the Event was published")
