import datetime
import pickle
import os.path

from django.conf import settings
from googleapiclient.discovery import build
from google.oauth2 import service_account

from . import constants
from . import models


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def google_publish_event(event):
    # Map our event to Google Calendar API v3
    payload = {
      'summary': event.title,
      'location': event.location,
      'description': event.description,
      'start': {
        'dateTime': event.start_datetime.isoformat(),
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': event.end_datetime.isoformat(),
        'timeZone': 'America/Los_Angeles',
      },
      #'recurrence': [
      #  'RRULE:FREQ=DAILY;COUNT=2'
      #],
      'visibility': 'private' if event.approval_status == constants.EventApprovalStatus.PENDING else 'public',
      #"extendedProperties": {
      #  "shared": {
      #    "petsAllowed": "yes"
      #  }
      #}
    }

    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)

    result = service.events().insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=payload).execute()
    print ('Event created: %s' % (result.get('htmlLink')))

    google_event = models.GoogleEvent(event=event, google_calendar_id=result['id'], published = datetime.datetime.now())
    google_event.save()
