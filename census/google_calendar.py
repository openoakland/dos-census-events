from datetime import datetime, timezone
import logging
import pickle
import os.path

from django.conf import settings
from django.contrib.sites.models import Site
from googleapiclient.discovery import build
from google.oauth2 import service_account

from . import constants
from . import models

log = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Helper method to get the service. Mostly to help with testing.
def get_service():
    credentials = service_account.Credentials.from_service_account_info(
        settings.GOOGLE_SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    return service


def google_publish_event(event):
    # Map our event to Google Calendar API v3
    payload = {
      'summary': event.title,
      'location': event.location,
      'description': event.description + "<a href=http://" +
      # need to provide the right domain for the server
      Site.objects.get_current().domain + "/event/" + str(event.id) +
          "/details> Event Details</a>",
      'start': {
        'dateTime': event.start_datetime.isoformat(),
        'timeZone': settings.TIME_ZONE,
      },
      'end': {
        'dateTime': event.end_datetime.isoformat(),
        'timeZone': settings.TIME_ZONE,
      },
      'recurrence': [str(event.recurrences)] if event.recurrences else None,
      'visibility': 'private' if event.approval_status == constants.EventApprovalStatus.PENDING else 'public',
      #"extendedProperties": {
      #  "shared": {
      #    "petsAllowed": "yes"
      #  }
      #}
    }

    service = get_service()

    google_event = models.GoogleEvent.objects.filter(event = event).first()
    # If the event is already in the calendar then we will update it
    if google_event is not None:
        log.debug('event update calendar=%s payload=%s', settings.GOOGLE_CALENDAR_ID, payload)
        log.info('event update event=%s title=%s', event.id, event.title)
        result = service.events().update(calendarId=settings.GOOGLE_CALENDAR_ID, eventId=google_event.google_calendar_id, body=payload).execute()
        google_event.published = datetime.now(tz=timezone.utc)
    else:
        # Event not in calendar insert it and record its ID there.
        log.debug('event insert calendar=%s payload=%s', settings.GOOGLE_CALENDAR_ID, payload)
        log.info('event insert event=%s title=%s', event.id, event.title)
        result = service.events().insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=payload).execute()
        google_event = models.GoogleEvent(event=event, google_calendar_id=result['id'], published = datetime.now(tz=timezone.utc))

    log.debug('google event result=%s', result)
    log.info('google event created/updated id=%s url=%s', result.get('id'), result.get('htmlLink'))
    google_event.save()

def google_delete_event(event):

    google_event = models.GoogleEvent.objects.filter(event = event).first()
    # If we have not pushed it then there is nothing to do.
    if google_event is None:
        return

    service = get_service()

    log.debug('event delete calendar=%s event=%s', settings.GOOGLE_CALENDAR_ID, google_event.google_calendar_id)
    log.info('event delete event=%s title=%s', event.id, event.title)
    result = service.events().delete(calendarId=settings.GOOGLE_CALENDAR_ID, eventId=google_event.google_calendar_id).execute()

    log.debug('google event result=%s', result)
    log.info('google event deleted  id=%s', google_event.google_calendar_id)
