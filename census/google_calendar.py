from datetime import datetime, timezone
import logging
import pickle
import os.path

from django.conf import settings
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
      'description': event.description,
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

    log.debug('event insert calendar=%s payload=%s', settings.GOOGLE_CALENDAR_ID, payload)
    log.info('event insert event=%s title=%s', event.id, event.title)
    result = service.events().insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=payload).execute()

    log.debug('google event result=%s', result)
    log.info('google event created id=%s url=%s', result.get('id'), result.get('htmlLink'))
    google_event = models.GoogleEvent(event=event, google_calendar_id=result['id'], published = datetime.now(tz=timezone.utc))
    google_event.save()
