from django.test import TestCase
from .models import Charge, Schedule, ScheduleLot, ScheduleCharge

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

class ScheduleToMinutesTest(TestCase):
    def setUp(self):
        self.sch = Schedule(schedule_lot=None, start=None, end=None)

    def test_one_hour(self):
        # prepare
        t1 = datetime(2016, 12, 24, 8)
        t2 = datetime(2016, 12, 24, 9)
        # do
        td = self.sch._to_minutes(t2 - t1)
        # check
        self.assertEqual(td, 60)

from django.utils import timezone
from datetime import datetime, timedelta

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

class ScheduleChargeTest(TestCase):
    def setUp(self):
        self.sch = Schedule.objects.create(schedule_lot=
                ScheduleLot.objects.create(name='Strefa A'), 
                start=timezone.now(), end=timezone.now())
        self.cha = []
        self.cha.append(Charge.objects.create(cost=1, minutes=61, duration=61))
        self.cha.append(Charge.objects.create(cost=1, minutes=62, duration=62))
        self.cha.append(Charge.objects.create(cost=1, minutes=63, duration=63))
        ScheduleCharge.objects.create(schedule=self.sch, charge=self.cha[0])
        ScheduleCharge.objects.create(schedule=self.sch, charge=self.cha[1])
        ScheduleCharge.objects.create(schedule=self.sch, charge=self.cha[2])

    def test_charges_in_order(self):
        # prepare
        charges = self.sch.charges.all()
        # do
        # check
        for i in range(0, len(self.cha)):
            self.assertEqual(charges[i], self.cha[i], msg='Wrong order')

    def test_reverse_order(self):
        # prepare
        charges = list(self.sch.charges.all().order_by('-schedulecharge__order'))
        # do
        # check
        for charge in self.cha:
            ch = charges.pop()
            self.assertEqual(ch, charge, msg='Wrong order')

from decimal import Decimal

class SchedulePriceCalculationTest(TestCase):
    def setUp(self):
        self.s_start = timezone.make_aware(datetime(2016, 12, 24, 8))
        self.s_end = timezone.make_aware(datetime(2016, 12, 24, 17))
        self.sch = Schedule.objects.create(
                schedule_lot=ScheduleLot.objects.create(name='Strefa A'),
                start=self.s_start,
                end=self.s_end)
           
    def charges1(self):
        ch = Charge.objects.create(cost=1.0, minutes=60, duration=60)
        ScheduleCharge.objects.create(schedule=self.sch, charge=ch)
        ch = Charge.objects.create(cost=2.0, minutes=120, duration=60)
        ScheduleCharge.objects.create(schedule=self.sch, charge=ch)
        ch = Charge.objects.create(cost=1.0, minutes=60, duration=60)

    def test_ticket_in_one_charge(self):
        # prepare
        self.charges1()
        t = Ticket(start=self.s_start, end=self.s_start + timedelta(minutes=60))
        # do
        sch = Schedule.objects.get()
        price = sch.calculate_price(t)
        # check
        self.assertEqual(price, Decimal('1.0'), msg='Price is wrong')

    def test_ticket_in_three_charges(self):
        # prepare
        self.charges1()
        t = Ticket(start=self.s_start + timedelta(hours=1),
                end=self.s_start + timedelta(hours=3, minutes=30))
        # do
        sch = Schedule.objects.get()
        price = sch.calculate_price(t)
        # check
        self.assertEqual(price, Decimal('2.5'), msg='Price is wrong')

    def test_ticket_start_before_end_after(self):
        # prepare
        self.charges1()
        t = Ticket(start=self.s_start - timedelta(minutes=45),
                end=self.s_end + timedelta(days=1))
        # do
        price = self.sch.calculate_price(t)
        # check
        self.assertEqual(price, Decimal('9.0'), msg='Price is wrong')

from schedule.models import Rule

class ScheduleLotTest(TestCase):
    def setUp(self):
        self.lot = ScheduleLot.objects.create(name='Strefa A')
        self.rule = Rule.objects.create(frequency='WEEKLY', name='weekly')
        self.s1_start = timezone.make_aware(datetime(2016, 12, 24, 8))
        self.s1_end = timezone.make_aware(datetime(2016, 12, 24, 17))
        self.sch1 = Schedule.objects.create(start=self.s1_start, end=self.s1_end,
                schedule_lot=self.lot, rule=self.rule)

    def test_get_related_schedules(self):
        # prepare
        # do
        schedules = self.lot.schedule_set.all()
        # check
        self.assertEqual(len(schedules), 1, msg='Wrong number of schedules')

    def test_get_schedule_from_one_day(self):
        # prepare
        t = Ticket(self.s1_start, self.s1_start + timedelta(hours=2))
        # do
        schedule = self.lot._get_schedule(t)
        # check
        self.assertEqual(schedule.start, self.s1_start, msg='Wrong schedule')

    def test_get_schedule_week_later(self):
        # prepare
        start = self.s1_start + timedelta(days=7)
        t = Ticket(start, start + timedelta(hours=2))
        # do
        schedule = self.lot._get_schedule(t)
        # check
        self.assertEqual(schedule.start, start, msg='Wrong schedule')

    def test_get_schedule_start_before_ends_in(self):
        # prepare
        t = Ticket(self.s1_start - timedelta(hours=1), self.s1_end - timedelta(hours=2))
        # do
        schedule = self.lot._get_schedule(t)
        # check
        self.assertEqual(schedule.start, self.s1_start, msg='Wrong schedule')

    def test_get_schedule_start_in_ends_in(self):
        # prepare
        t = Ticket(self.s1_start + timedelta(hours=2), self.s1_end - timedelta(hours=2))
        # do
        schedule = self.lot._get_schedule(t)
        # check
        self.assertEqual(schedule.start, self.s1_start, msg='Wrong schedule')

    def test_get_schedule_start_in_ends_after(self):
        # prepare
        t = Ticket(self.s1_start + timedelta(hours=3), self.s1_end + timedelta(hours=2))
        # do
        schedule = self.lot._get_schedule(t)
        # check
        self.assertEqual(schedule.start, self.s1_start, msg='Wrong schedule')

class ScheduleLotPriceCalculationTest(TestCase):
    def setUp(self):
        self.lot = ScheduleLot.objects.create(name='Strefa A')
        self.start = timezone.make_aware(datetime(2016, 12, 25, 8))
        self.end = timezone.make_aware(datetime(2016, 12, 25, 17))
        self.rule = Rule.objects.create(frequency='WEEKLY', name='weekly')
        self.sch = Schedule.objects.create(start=self.start, end=self.end,
                rule=self.rule, schedule_lot=self.lot)
        self.cha = Charge.objects.create(cost=1, minutes=60, duration=60)
        ScheduleCharge.objects.create(schedule=self.sch, charge=self.cha)

    def test_price_calculation(self):
        # prepare
        t = Ticket(self.start, self.end)
        # do
        price = self.lot.calculate_price(t)
        # check
        self.assertEqual(price, Decimal('9.0'), msg='Price is wrong')

