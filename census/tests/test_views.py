from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth import views as auth_views

from census import views

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
    def setUp(self):
        self.url = "/pending/"

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.view_class, views.PendingList.as_view().view_class)


class CensusUpdateViewTest(TestCase):
    def setUp(self):
        self.url = "/1/update/"

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func.view_class, views.UpdateEvent.as_view().view_class)


class CensusDeleteViewTest(TestCase):
    def setUp(self):
        self.url = "/1/delete/"

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