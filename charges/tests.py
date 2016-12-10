from django.test import TestCase
from schedule.models import Event
from schedule.periods import Period
from django.utils import timezone
import datetime

class UsersTest(TestCase):

    def setUp(self):
        self.parking_start = timezone.make_aware(datetime.datetime(2016, 12, 10, 8))
        self.parking_end = timezone.make_aware(datetime.datetime(2016, 12, 10, 17))
        
    def test_event_start_in_period(self):
        # prepare
        period_start = timezone.make_aware(datetime.datetime(2016, 12, 10, 7))
        period_end = timezone.make_aware(datetime.datetime(2016, 12, 10, 9))

        event = Event(start=self.parking_start, end=self.parking_end)
        period = Period([event], start=period_start, end=period_end)
        # do
        occr = period.get_occurrences()
        clssify = period.classify_occurrence(occr[0])
        # check
        self.assertTrue(clssify['class'] == 0, msg='Event did not started in period')

    def test_event_end_in_period(self):
        # prepare
        period_start = timezone.make_aware(datetime.datetime(2016, 12, 10, 16))
        period_end = timezone.make_aware(datetime.datetime(2016, 12, 10, 18))

        event = Event(start=self.parking_start, end=self.parking_end)
        period = Period([event], start=period_start, end=period_end)
        # do
        occr = period.get_occurrences()
        clssify = period.classify_occurrence(occr[0])
        # check
        self.assertTrue(clssify['class'] == 3, msg='Event did not ended in period')
 
