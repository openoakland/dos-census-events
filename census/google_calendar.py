import datetime
import pickle
import os.path

from django.conf import settings
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    result = service.events().insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=payload).execute()
    print ('Event created: %s' % (result.get('htmlLink')))

    google_event = models.GoogleEvent(event=event, google_calendar_id=result['id'], published = datetime.datetime.now())
    google_event.save()
