from datetime import datetime
import logging
from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from pytz import timezone
import recurrence

from census import constants, google_calendar
from census.models import Event, GoogleEvent
import census.tests.factory as factory


#TODO should this live somewhere else?
def setUpModule():
    logging.disable(logging.WARNING)


def tearDownModule():
    logging.disable(logging.NOTSET)


class GooglePublishCommandTest(TestCase):
    @mock.patch('census.google_calendar.google_publish_event')
    def test_approved_events(self, mock_google_publish_event):
        """Given an approved event, the event should be published"""

        approved_event = factory.event(approval_status=constants.EventApprovalStatus.APPROVED)
        approved_event.save()

        call_command('google_publish')

        mock_google_publish_event.assert_called_with(approved_event)


    @mock.patch('census.google_calendar.google_publish_event')
    def test_pending_events(self, mock_google_publish_event):
        """Given pending event, the event should not be published"""

        pending_event = factory.event(approval_status=constants.EventApprovalStatus.PENDING)
        pending_event.save()

        call_command('google_publish')

        mock_google_publish_event.assert_not_called()


    @mock.patch('census.google_calendar.google_publish_event')
    def test_published_events(self, mock_google_publish_event):
        """Given a published event, the event should not be re-published"""

        event = factory.event()
        event.save()
        published_event = factory.google_event(event=event)
        published_event.save()

        call_command('google_publish')

        mock_google_publish_event.assert_not_called()


class GoogleCalendarPublishEvent(TestCase):
    def setUp(self):
        # Setup some complex stubbing
        self.expected_response = dict(id='123', htmlLink='http://example.com/event123')
        #self.mock_events = mock.Mock(insert=mock.Mock(return_value=self.expected_response))
        #self.mock_service = mock.Mock(events=self.mock_events)
        self.mock_insert = mock.Mock()
        self.mock_insert.execute = mock.Mock(return_value=self.expected_response)
        self.mock_events = mock.Mock()
        self.mock_events.insert = mock.Mock(return_value=self.mock_insert)
        self.mock_service = mock.Mock()
        self.mock_service.events = mock.Mock(return_value=self.mock_events)

    def test_event(self):
        """Given an event, Google Calendar payload contains event information"""

        event = factory.event()
        event.save()

        with mock.patch('census.google_calendar.get_service', return_value=self.mock_service):
            google_calendar.google_publish_event(event)

        self.mock_service.events.assert_called_with()
        self.mock_events.insert.assert_called_once()
        payload = self.mock_events.insert.call_args[1]['body']

        self.assertEqual(payload['summary'], event.title)
        self.assertTrue(payload['description'].startswith(event.description))
        self.assertEqual(payload['start']['dateTime'], event.start_datetime.isoformat())
        self.assertEqual(payload['start']['timeZone'], 'America/Los_Angeles')
        self.assertEqual(payload['end']['dateTime'], event.end_datetime.isoformat())
        self.assertEqual(payload['end']['timeZone'], 'America/Los_Angeles')
        self.assertEqual(payload['visibility'], 'public')
        self.assertFalse('recurrences' in payload)

        google_events = GoogleEvent.objects.all()
        assert len(google_events) == 1

        google_event = google_events[0]
        self.assertEqual(google_event.google_calendar_id, self.expected_response['id'])
        self.assertEqual(google_event.event.id, event.id)
        # TODO Stub datetime.now
        #assert google_event.published == expected_published


    def test_pending_event(self):
        """Given a pending event, Google Calendar payload contains visibility private"""

        event = factory.event(approval_status=constants.EventApprovalStatus.PENDING)
        event.save()

        with mock.patch('census.google_calendar.get_service', return_value=self.mock_service):
            google_calendar.google_publish_event(event)

        self.mock_service.events.assert_called_with()
        self.mock_events.insert.assert_called_once()
        payload = self.mock_events.insert.call_args[1]['body']

        self.assertEqual(payload['visibility'], 'private')


    def test_recurring_event(self):
        """Given a recurring event, Google Calendar payload contains recurrence"""

        event = factory.event(recurrences=recurrence.Recurrence(rrules=[recurrence.Rule(recurrence.DAILY)]))
        event.save()

        with mock.patch('census.google_calendar.get_service', return_value=self.mock_service):
            google_calendar.google_publish_event(event)

        self.mock_service.events.assert_called_with()
        self.mock_events.insert.assert_called_once()
        payload = self.mock_events.insert.call_args[1]['body']

        self.assertEqual(payload['recurrence'], ['RRULE:FREQ=DAILY'])
