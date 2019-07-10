import logging


from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from census.models import Event, GoogleEvent
from census.google_calendar import google_publish_event



class Command(BaseCommand):
    help = 'Publishes any approved events not already published to the Google Calendar.'

    def handle(self, *args, **options):
        # TODO optimize the SQL query
        for event in Event.objects.all():
            try:
                event.google_event
            except ObjectDoesNotExist:
                # This is okay, the GoogleEvent will be created when published.
                pass
            else:
                # GoogleEvent exists, so it's already published. We should skip.
                continue

            google_publish_event(event)

            #google_event = None
            #try:
            #    google_event = GoogleEvent.objects.get(event=event)
            #except ObjectDoesNotExist:
            #    # This is okay, the GoogleEvent will be created when published.
            #    pass

            #if google_event:
            #    # Already published, skip
            #    continue

            #google_publish_event(event)
