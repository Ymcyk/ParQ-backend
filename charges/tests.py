from django.test import TestCase
from .models import Charge, Schedule, ScheduleLot

class ChargesTest(TestCase):
    def setUp(self):
        self.ch1 = Charge.objects.create(cost=2.0, minutes=60, duration=60)
        self.ch2 = Charge.objects.create(cost=2.0, minutes=60, duration=60,
                minute_billing=False)

    def test_full_minutes(self):
        # prepare
        ch1 = Charge.objects.get(id=1)
        # do
        price = ch1.calculate_price(ch1.minutes)
        # check
        self.assertEqual(price, ch1.cost, msg='Price not equal cost')

    def test_half_minutes(self):
        # prepare
        ch1 = Charge.objects.get(id=1)
        # do
        price = ch1.calculate_price(ch1.minutes // 2)
        # check
        self.assertEqual(ch1.cost / 2, price, msg='Price not equal half cost')

    def test_quarter_minutes(self):
        # prepare
        ch1 = Charge.objects.get(id=1)
        # do
        price = ch1.calculate_price(ch1.minutes // 4)
        # check
        self.assertEqual(ch1.cost / 4, price, msg='Price not equal quarter cost')

    def test_double_minutes(self):
        # prepare
        ch1 = Charge.objects.get(id=1)
        # do
        price = ch1.calculate_price(ch1.minutes * 2)
        # check
        self.assertEqual(ch1.cost * 2, price, msg='Price not equal double cost')

    def test_minute_billing_less_than_minutes(self):
        # prepare
        ch2 = Charge.objects.get(id=2)
        # do
        price = ch2.calculate_price(ch2.minutes - 1)
        # check
        self.assertEqual(price, ch2.cost, msg='Price not equal cost')

    def test_minute_billing_more_than_minutes(self):
        # prepare
        ch2 = Charge.objects.get(id=2)
        # do
        price = ch2.calculate_price(ch2.minutes + 2)
        # check
        self.assertEqual(price, ch2.cost * 2, msg='Price not equal cost')

from django.utils import timezone
from datetime import datetime

class Ticket:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class ScheduleEffectiveDatesTest(TestCase):
    
    def setUp(self):
        self.t1 = Ticket(timezone.make_aware(datetime(2016, 12, 24, 7)), 
                timezone.make_aware(datetime(2016, 12, 24, 9)))
        self.t2 = Ticket(timezone.make_aware(datetime(2016, 12, 24, 9)), 
                timezone.make_aware(datetime(2016, 12, 24, 10)))
        self.t3 = Ticket(timezone.make_aware(datetime(2016, 12, 24, 16)), 
                timezone.make_aware(datetime(2016, 12, 24, 18)))
        self.t4 = Ticket(timezone.make_aware(datetime(2016, 12, 24, 18)), 
                timezone.make_aware(datetime(2016, 12, 24, 20)))
        self.sch = Schedule.objects.create(schedule_lot=
            ScheduleLot.objects.create(name='Strefa A'), start=timezone.make_aware(
            datetime(2016, 12, 24, 8)), end=timezone.make_aware(
            datetime(2016, 12, 24, 17))) 

    def test_start_before_end_in_schedule(self):
        # prepare
        sch = Schedule.objects.get()
        # do
        dates = sch._get_effective_dates(self.t1)
        # check
        test = dates[0] == sch.start and dates[1] == self.t1.end
        self.assertTrue(test)

    def test_start_in_end_in_schedule(self):
        # prepare
        sch = Schedule.objects.get()
        # do
        dates = sch._get_effective_dates(self.t2)
        # check
        test = dates[0] == self.t2.start and dates[1] == self.t2.end
        self.assertTrue(test)

    def test_start_in_end_after_schedule(self):
        # prepare
        sch = Schedule.objects.get()
        # do
        dates = sch._get_effective_dates(self.t3)
        # check
        test = dates[0] == self.t3.start and dates[1] == sch.end
        self.assertTrue(test)

    def test_start_after_schedule(self):
        # prepare
        sch = Schedule.objects.get()
        # do
        # check
        with self.assertRaises(Exception, msg='Exception not raised'):
            sch._get_effective_dates(self.t4)