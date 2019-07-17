import logging


from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from census.models import Event, GoogleEvent
from census.google_calendar import google_publish_event

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Publishes any approved events not already published to the Google Calendar.'

    def handle(self, *args, **options):
        # TODO optimize the SQL query
        log.info('starting publish...')
        for event in Event.objects.all():
            try:
                event.google_event
            except ObjectDoesNotExist:
                # This is okay, the GoogleEvent will be created when published.
                pass
            else:
                # GoogleEvent exists, so it's already published. We should skip.
                log.debug('event already published event=%s', event.id)
                continue

            log.info('event not yet published event=%s', event.id)
            google_publish_event(event)
