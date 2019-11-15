from django.urls import reverse, resolve
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import views as auth_views

from census import views
from census import constants
from census.models import Event

class CensusExportViewTest(TestCase):
    def setUp(self):
        self.url = "/export/events/"

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, views.export_events)

class CensusSubmitViewTest(TestCase):
    def setUp(self):
        self.url = "/submit/"

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, views.add_event)


class CensusPendingViewTest(TestCase):
    fixtures = ["census/fixtures/events.json"]
    def setUp(self):
        self.url = "/pending/"
        self.client = Client()

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
        for event in pending_events:
            self.assertEqual(event.approval_status, constants.EventApprovalStatus.PENDING.name)

    def test_template_content(self):
        event = Event.objects.filter(approval_status=constants.EventApprovalStatus.PENDING.name).first()
        response = self.client.get(self.url)
        
        # Response contains the title of a pending event
        self.assertContains(response, event.title)

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