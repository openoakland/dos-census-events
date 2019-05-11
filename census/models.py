from django.db import models

from . import constants


class Event(models.Model):
    title = models.CharField(max_length=100, help_text="Title or short description of the event")
    description = models.TextField(help_text="Full description of the event")
    start_datetime = models.DateTimeField(help_text="When does this event start?")
    end_datetime = models.DateTimeField(help_text="When does the event end?", null=True, blank=True)
    organization_name = models.CharField(max_length=100, help_text="Name of the hosting organization")
    EVENT_TYPE_CHOICES = (
        ("WORKSHOP", 'Workshop'),
        ("TABLING", 'Tabling'),
        ("CELEBRATION", 'Celebration'),
        ("DROPIN", 'Drop-in center'),
        ("OTHER", 'Other')
    )
    event_type = models.CharField(
        max_length=255,
        choices=EVENT_TYPE_CHOICES, 
        default="OTHER",)
    ## TODO: Make a more precise location that can be used to lookup geocode
    location = models.CharField(max_length=100, help_text="Location where the event will take place")
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_census_equipped = models.BooleanField(help_text="Is this event technologically equipped to allow people to take the census?")
    APPROVAL_STATUS_CHOICES = (
        ("PENDING", 'Pending'),
        ("APPROVED", 'Approved'),
    )
    approval_status = models.CharField(
        max_length=255,
        choices=APPROVAL_STATUS_CHOICES, 
        default="PENDING",)
