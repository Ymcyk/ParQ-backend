from django.test import TestCase
from schedule.models import Event
from schedule.periods import Period
from django.utils import timezone
import datetime

from .models import *

class UsersTest(TestCase):

    def setUp(self):
        self.parking_start = timezone.make_aware(datetime.datetime(2016, 12, 10, 8))
        self.parking_end = timezone.make_aware(datetime.datetime(2016, 12, 10, 17))
        self.tariff1 = Tariff.objects.create(cost=1.5, minutes=60)
        self.schedule_lot1 = ScheduleLot.objects.create(name='Strefa A')
        self.schedule1 = Schedule.objects.create(start=self.parking_start,
                end=self.parking_end, schedule_lot=self.schedule_lot1)
        self.charge1 = Charge.objects.create(tariff=self.tariff1, 
                duration=datetime.timedelta(minutes=120), schedule=self.schedule1)
        self.charge2 = Charge.objects.create(tariff=self.tariff1, 
                duration=datetime.timedelta(minutes=120), schedule=self.schedule1)
        self.charge3 = Charge.objects.create(tariff=self.tariff1, 
                duration=datetime.timedelta(minutes=120), schedule=self.schedule1)

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
 
    def test_charges_in_schedule_are_numerated(self):

