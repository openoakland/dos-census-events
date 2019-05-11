from django.db import models

from . import constants


class Event(models.Model):
    title = models.CharField(max_length=100, help_text="Title or short description of the event")
    description = models.TextField(help_text="Full description of the event")
    start_datetime = models.DateTimeField(help_text="When does this event start?")
    end_datetime = models.DateTimeField(help_text="When does the event end?")
    organization_name = models.CharField(max_length=100, help_text="Name of the hosting organization")
    event_type = models.CharField(max_length=2, choices=[(t, t.value) for t in constants.EventType])
    location = models.CharField(max_length=100, help_text="Location where the event will take place")
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    is_census_equipped = models.BooleanField(help_text="Is this event technologically equipped to allow people to take the census?")
    approval_status = models.CharField(max_length=2, choices=[(t, t.value) for t in constants.EventApprovalStatus])
