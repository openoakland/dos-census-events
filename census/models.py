from django.db import models
from recurrence.fields import RecurrenceField
from multiselectfield import MultiSelectField

from . import constants

#class EventManager(models.Manager):
#    def get_queryset(self):
#        '''
#        Filter out pending events by default. If you need pending and active,
#        use Event.with_pending instead of Event.objects.
#        '''
#        return super(EventManager, self).get_queryset().filter(approval_status=constants.EventApprovalStatus.APPROVED)


class Event(models.Model):

    def __str__(self):
        return self.title

    def first_date(self):
        return self.recurrences.occurrences()[0].date()

    title = models.CharField(max_length=100, help_text="Title or short description of the event")
    description = models.TextField(blank=True, help_text="Full description of the event")
    recurrences  = RecurrenceField(default=None, blank=True, verbose_name='Date Information', help_text="Add date of the event or rules for a recurring event")
    start_time = models.TimeField(help_text="What time does this event start? HH:MM:AM/PM")
    end_time = models.TimeField(help_text="What time does the event end? HH:MM:AM/PM")
    organization_name = models.CharField(max_length=100, help_text="Name of the hosting organization")
    event_type = models.CharField(max_length=20, choices=[(t.name, t.value) for t in constants.EventType])
    location = models.CharField(max_length=100, help_text="Location where the event will take place")
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default=None)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default=None)
    is_census_equipped = models.BooleanField(default=False, help_text="Is this event technologically equipped to allow people to take the census?")
    approval_status = models.CharField(max_length=20, default=constants.EventApprovalStatus.PENDING, choices=[(t.name, t.value) for t in constants.EventApprovalStatus])
    languages = MultiSelectField(choices=[(t.name, t.value) for t in constants.Languages])

    # If you need pending and active, use Event.with_pending instead of Event.objects
    #with_pending = models.Manager()

class GoogleEvent(models.Model):
    google_calendar_id = models.CharField(max_length=100)
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='google_event')
    published = models.DateTimeField(help_text="Time when the Event was published")
