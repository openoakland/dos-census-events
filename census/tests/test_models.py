from datetime import date

from django.test import TestCase

from census.models import Event

class EventTest(TestCase):
    fixtures=["census/fixtures/events.json"]
    def setUp(self):
        # Get an event that has recurrences
        self.event = [event for event in Event.objects.all() if event.recurrences.rrules][0]

    def test_first_date(self):
        first_date = self.event.first_date()
        self.assertIsInstance(first_date, date)

        self.event.recurrences.rrules = []
        self.event.save()

        first_date = self.event.first_date()
        self.assertIs(first_date, None)