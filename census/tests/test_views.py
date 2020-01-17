import logging
from datetime import datetime, timedelta
from unittest.mock import ANY

import pytz
import recurrence
from django.contrib.auth import views as auth_views
from django.test import TestCase, RequestFactory, Client
from django.urls import resolve

from census import constants
from census import views
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
        self.assertTemplateUsed(response, 'census/event_form.html')

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
            city="Oakland",
            zip_code="94612",
            event_type="Workshop",
            languages="English",
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
        self.assertEqual(event.languages, [constants.Languages.ENGLISH])
        self.assertEqual(event.city, data['city'])
        self.assertEqual(event.zip_code, data['zip_code'])
        # There is an implicit assumption server time is America/Los_Angeles
        self.assertEqual(event.start_datetime.timestamp(), datetime(2019, 11, 15, 15, 0).astimezone(los_angeles).timestamp())
        self.assertEqual(event.end_datetime.timestamp(), datetime(2019, 11, 15, 16, 0).astimezone(los_angeles).timestamp())

        # The event has the right defaults
        self.assertEqual(event.recurrences, recurrence.Recurrence())
        self.assertEqual(event.approval_status, constants.EventApprovalStatus.PENDING)


    def test_submit_without_start_fails(self):
        """Given the submit event form is missing start datetime, the submission fails"""
        data = dict(
            title="OpenOakland Hack Night",
            description="Civic technology event",
            organization_name="OpenOakland",
            location="City Hall",
            city="Oakland",
            zip_code="94612",
            event_type="Workshop",
            languages="English",
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
            city="Oakland",
            zip_code="94612",
            event_type="Workshop",
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
            city="Oakland",
            zip_code="94612",
            event_type="Workshop",
            languages="English",
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

    def test_contact_not_required(self):
        data = dict(
            title="OpenOakland Hack Night",
            description="Civic technology event",
            organization_name="OpenOakland",
            location="City Hall",
            city="Oakland",
            zip_code="94612",
            event_type="Workshop",
            languages="English",
            start_datetime="2019-11-15 15:00",
            end_datetime="2019-11-15 16:00",
            recurrences="",
        )

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)

        event = Event.objects.all()[0]
        self.assertEqual(event.contact_email, None)
        self.assertEqual(event.contact_name, None)
        self.assertEqual(event.contact_phone, None)



class CensusPendingViewTest(TestCase):
    """Test pending list view returns a single pending event."""
    def setUp(self):
        self.url = "/pending/"
        self.client = Client()
        self.pending_event = factory.event(approval_status=constants.EventApprovalStatus.PENDING)
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

class CensusApprovedViewTest(TestCase):
    """Test approved  list view returns a single approved event."""
    def setUp(self):
        self.url = "/approved/"
        self.client = Client()
        self.approved_event = factory.event(approval_status=constants.EventApprovalStatus.APPROVED)
        self.approved_event.save()

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.view_class, views.ApprovedList.as_view().view_class)

    def test_get_approved(self):
        factory = RequestFactory()
        request = factory.get(self.url)
        results = views.ApprovedList.as_view()(request)
        approved_events = results.context_data["event_list"]

        # Assumes 1 approved event in initial test data
        self.assertEqual(len(approved_events), 1)
        event = approved_events[0]
        self.assertEqual(event, self.approved_event)

    def test_template_content(self):
        response = self.client.get(self.url)

        # Response contains the title of a approved event
        self.assertContains(response, self.approved_event.title)

class CensusPendingViewWithRecurrenceTest(TestCase):
    """Given a recurring pending event, the event appears in the pending list"""

    def setUp(self):
        self.url = "/pending/"
        self.client = Client()
        self.pending_event = factory.event(
            approval_status=constants.EventApprovalStatus.PENDING,
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


class CensusHomepageViewTest(TestCase):
    def setUp(self):
        self.url = '/'
        self.client = Client()

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.view_class, views.HomepageView.as_view().view_class)

    def test_get(self):
        current_date = datetime.now()
        localized_time = los_angeles.localize(current_date)
        self.approved_event = factory.event(start_datetime=localized_time,
                                            end_datetime=localized_time+timedelta(hours=2))
        self.approved_event.save()

        response = self.client.get(self.url)

        start_datetime = self.approved_event.start_datetime.astimezone(los_angeles)
        end_datetime = self.approved_event.end_datetime.astimezone(los_angeles)
        assert response.context['request'].events == [
            (self.approved_event.start_datetime.strftime('%A, %B %d'),
             [{'id': ANY,
               'title': self.approved_event.title,
               'description': self.approved_event.description,
               'month': localized_time.month,
               'start_date': datetime.strftime(start_datetime, "%Y-%m-%d"),
               'end_date': datetime.strftime(end_datetime, "%Y-%m-%d"),
               'start_time': datetime.strftime(start_datetime, "%I:%M %p"),
               'end_time': datetime.strftime(end_datetime, "%I:%M %p"),
               'is_private_event': False,
               }
              ]),
        ]

    def test_get_with_query_params(self):
        current_date = datetime.now()
        localized_time = los_angeles.localize(current_date)
        self.approved_event = factory.event(start_datetime=localized_time,
                                            end_datetime=localized_time + timedelta(hours=2))
        self.approved_event.save()

        data = {
            'isMonthly': 'false',
            'day': current_date.day,
            'month': current_date.month,
            'year': current_date.year
        }
        response = self.client.get(self.url, data)

        start_datetime = self.approved_event.start_datetime.astimezone(los_angeles)
        end_datetime = self.approved_event.end_datetime.astimezone(los_angeles)
        assert response.context['request'].events == [
            (self.approved_event.start_datetime.strftime('%A, %B %d'),
             [{'id': ANY,
               'title': self.approved_event.title,
               'description': self.approved_event.description,
               'month': localized_time.month,
               'start_date': datetime.strftime(start_datetime, "%Y-%m-%d"),
               'end_date': datetime.strftime(end_datetime, "%Y-%m-%d"),
               'start_time': datetime.strftime(start_datetime, "%I:%M %p"),
               'end_time': datetime.strftime(end_datetime, "%I:%M %p"),
               'is_private_event': False,
               }]),
        ]

    def test_get_monthly_results(self):
        current_date = datetime.now().replace(month=3)
        localized_time = los_angeles.localize(current_date)
        self.approved_event = factory.event(start_datetime=localized_time,
                                            end_datetime=localized_time + timedelta(hours=2))
        self.approved_event.save()

        data = {
            'isMonthly': 'true',
            'month': 3,
            'year': current_date.year
        }
        response = self.client.get(self.url, data)

        start_datetime = self.approved_event.start_datetime.astimezone(los_angeles)
        end_datetime = self.approved_event.end_datetime.astimezone(los_angeles)
        assert response.context['request'].events == [
            (self.approved_event.start_datetime.strftime('%A, %B %d'),
             [{'id': ANY,
               'title': self.approved_event.title,
               'description': self.approved_event.description,
               'month': localized_time.month,
               'start_date': datetime.strftime(start_datetime, "%Y-%m-%d"),
               'end_date': datetime.strftime(end_datetime, "%Y-%m-%d"),
               'start_time': datetime.strftime(start_datetime, "%I:%M %p"),
               'end_time': datetime.strftime(end_datetime, "%I:%M %p"),
               'is_private_event': False,
               }]),
        ]

    def test_get_search_query(self):
        current_date = datetime.now()
        localized_time = los_angeles.localize(current_date)
        self.approved_event = factory.event(start_datetime=localized_time,
                                            end_datetime=localized_time + timedelta(hours=2))

        self.approved_event.save()
        self.approved_event_two = factory.event(title="some title")
        self.approved_event_two.save()

        response = self.client.get(self.url, {'search': 'oak'})

        assert len(response.context['request'].events) == 1
        assert len(response.context['request'].events[0][1]) == 1
        assert response.context['request'].events[0][1][0]['title'] == self.approved_event.title
