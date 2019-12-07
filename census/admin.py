from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (
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
        'lat',
        'lon',
        'approval_status',
        'contact_name',
        'contact_email',
        'contact_phone',
        'is_private_event'
    )
    list_display = ('title', 'start_datetime', 'end_datetime', 'recurrences', 'location')
