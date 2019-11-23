from datetime import datetime
import logging

from django.urls import reverse, resolve
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import views as auth_views
import pytz
import recurrence

from census import views
from census import constants
from census.models import Event
from census.tests import factory

los_angeles = pytz.timezone('America/Los_Angeles')


#TODO should this live somewhere else?
def setUpModule():
    logging.disable(logging.WARNING)


def tearDownModule():
    logging.disable(logging.NOTSET)


class CensusExportViewTest(TestCase):
    def setUp(self):
        self.url = "/export/events/"

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, views.export_events)

class CensusSubmitViewTest(TestCase):
    def setUp(self):
        self.url = "/submit/"
        self.client = Client()


    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.view_class, views.SubmitEventView.as_view().view_class)


    def test_required_fields_exist(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_form.html')

        # Maybe there's a more accurate way to test for input elements
        self.assertContains(response, 'name="languages"')
        self.assertContains(response, 'name="start_datetime"')
        self.assertContains(response, 'name="end_datetime"')
        self.assertContains(response, 'name="recurrences"')
        self.assertContains(response, 'name="contact_name"')
        self.assertContains(response, 'name="contact_email"')
        self.assertContains(response, 'name="contact_phone"')


    def test_submit(self):
        data = dict(
            title="OpenOakland Hack Night",
            description="Civic technology event",
            organization_name="OpenOakland",
            location="City Hall",
            event_type="WORKSHOP",
            languages="ENGLISH",
            start_datetime="2019-11-15 15:00",
            end_datetime="2019-11-15 16:00",
            recurrences="",
            contact_email="hi@example.com",
            contact_name="Kevin Man",
            contact_phone="510-523-4567",
        )

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)

        # The event was created
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.all()[0]

        # The event created in the database matches the data we submitted
        self.assertEqual(event.title, data['title'])
        self.assertEqual(event.description, data['description'])
        self.assertEqual(event.organization_name, data['organization_name'])
        self.assertEqual(event.location, data['location'])
        self.assertEqual(event.event_type, data['event_type'])
        self.assertEqual(event.languages, [constants.Languages.ENGLISH.name])
        # There is an implicit assumption server time is America/Los_Angeles
        self.assertEqual(event.start_datetime.timestamp(), datetime(2019, 11, 15, 15, 0).astimezone(los_angeles).timestamp())
        self.assertEqual(event.end_datetime.timestamp(), datetime(2019, 11, 15, 16, 0).astimezone(los_angeles).timestamp())

        # The event has the right defaults
        self.assertEqual(event.recurrences, recurrence.Recurrence())
        self.assertEqual(event.approval_status, constants.EventApprovalStatus.PENDING.name)


    def test_submit_without_start_fails(self):
        """Given the submit event form is missing start datetime, the submission fails"""
        data = dict(
            title="OpenOakland Hack Night",
            description="Civic technology event",
            organization_name="OpenOakland",
            location="City Hall",
            event_type="WORKSHOP",
            languages="ENGLISH",
            end_datetime="2019-11-15 16:00",
            recurrences="",
            contact_email="hi@example.com",
            contact_name="Kevin Man",
            contact_phone="510-523-4567",
        )

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

        form = response.context['form']
        self.assertIn('start_datetime', form.errors)


    def test_submit_without_languages_fails(self):
        """Given the submit event form is missing languages, the submission fails"""
        data = dict(
            title="OpenOakland Hack Night",
            description="Civic technology event",
            organization_name="OpenOakland",
            location="City Hall",
            event_type="WORKSHOP",
            languages="",
            start_datetime="2019-11-15 15:00",
            end_datetime="2019-11-15 16:00",
            recurrences="",
            contact_email="hi@example.com",
            contact_name="Kevin Man",
            contact_phone="510-523-4567",
        )

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

        form = response.context['form']
        self.assertIn('languages', form.errors)


    def test_submit_with_recurrence(self):
        """Given the submit event form includes recurrence, the recurrence is added to the database"""
        data = dict(
            title="OpenOakland Hack Night",
            description="Civic technology event",
            organization_name="OpenOakland",
            location="City Hall",
            event_type="WORKSHOP",
            languages="ENGLISH",
            start_datetime="2019-11-15 15:00",
            end_datetime="2019-11-15 16:00",
            recurrences="RRULE:FREQ=WEEKLY;BYDAY=TU",
            contact_email="hi@example.com",
            contact_name="Kevin Man",
            contact_phone="510-523-4567",
        )

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)

        # The event was created
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.all()[0]

        # The event created in the database matches the data we submitted
        self.assertEqual(str(event.recurrences), data['recurrences'])


class CensusPendingViewTest(TestCase):
    """Test pending list view returns a single pending event."""
    def setUp(self):
        self.url = "/pending/"
        self.client = Client()
        self.pending_event = factory.event(approval_status=constants.EventApprovalStatus.PENDING.name)
        self.pending_event.save()

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.view_class, views.PendingList.as_view().view_class)

    def test_get_pending(self):
        factory = RequestFactory()
        request = factory.get(self.url)
        results = views.PendingList.as_view()(request)
        pending_events = results.context_data["event_list"]

        # Assumes 1 pending event in initial test data
        self.assertEqual(len(pending_events), 1)
        event = pending_events[0]
        self.assertEqual(event, self.pending_event)

    def test_template_content(self):
        response = self.client.get(self.url)

        # Response contains the title of a pending event
        self.assertContains(response, self.pending_event.title)

class CensusPendingViewWithRecurrenceTest(TestCase):
    """Given a recurring pending event, the event appears in the pending list"""

    def setUp(self):
        self.url = "/pending/"
        self.client = Client()
        self.pending_event = factory.event(
            approval_status=constants.EventApprovalStatus.PENDING.name,
            recurrences=recurrence.Recurrence(rrules=[recurrence.Rule(recurrence.DAILY)]),
        )
        self.pending_event.save()

    def test_template_contains_recurrence(self):
        response = self.client.get(self.url)

        # Response contains the title of a pending event
        self.assertContains(response, self.pending_event.title)
        # Response contains the recurrence rule
        self.assertContains(response, 'daily')


class CensusUpdateViewTest(TestCase):
    def setUp(self):
        self.url = "/event/1/update/"

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.view_class, views.UpdateEvent.as_view().view_class)


class CensusDeleteViewTest(TestCase):
    def setUp(self):
        self.url = "/event/1/delete/"

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.view_class, views.DeleteEvent.as_view().view_class)


class CensusDeleteViewTest(TestCase):
    def setUp(self):
        self.url = "/login/"

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.view_class, auth_views.LoginView.as_view().view_class)


class CensusDeleteViewTest(TestCase):
    def setUp(self):
        self.url = "/logout/"

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.view_class, auth_views.LogoutView.as_view().view_class)
