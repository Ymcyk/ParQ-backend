from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from schedule.models import Rule
from djroles.models import Role
from badges.models import Badge, Vehicle
from parkings.models import Parking, Ticket
from users.models import Driver, Officer

from .models import Charge, Schedule, ScheduleLot, ScheduleCharge

class ViewTest(TestCase):
    def setUp(self):
        lot = ScheduleLot.objects.create(name='Zwykły taryfikator')
        self.parking = Parking.objects.create(name='Strefa A', 
                schedule_lot=lot)

        now = timezone.now()
        self.p_start = timezone.make_aware(datetime(now.year, now.month, now.day, 0, 1))
        self.p_end = timezone.make_aware(datetime(now.year, now.month, now.day, 23, 59))
        print('p_start:', self.p_start)
        print('p_end:', self.p_end)
        rule = Rule.objects.create(frequency='WEEKLY', name='weekly')
        self.schedule = Schedule.objects.create(schedule_lot=lot,
        start=self.p_start, end=self.p_end, rule=rule)

        self.ch1 = Charge.objects.create(cost=.7, minutes=15, duration=15, minute_billing=False)
        ScheduleCharge.objects.create(schedule=self.schedule, charge=self.ch1)

        self.ch2 = Charge.objects.create(cost=2.8, minutes=60, duration=60)
        ScheduleCharge.objects.create(schedule=self.schedule, charge=self.ch2)

        self.ch3 = Charge.objects.create(cost=3.2, minutes=60, duration=60)
        ScheduleCharge.objects.create(schedule=self.schedule, charge=self.ch3)

        self.password = 'test'
        self.user = User.objects.create_user(username='Jan', password=self.password, email='test@test.com')
        role = Role.objects.create_role(name='Driver')
        self.driver = Driver.objects.create(user=self.user)
        self.badge = Badge.objects.create()
        self.vehicle = Vehicle.objects.create(owner=self.driver, badge=self.badge,
            plate_number='ZS12345', plate_country='PL', name='Golf')

    def get_token(self):
        self.client = APIClient()
        response = self.client.post('/api/login/', {'username': self.user.username, 'password': self.password, 'role': 'driver'})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token) 

    def test_check_schedule_for_today(self):
        # prepare
        self.get_token()
        # do
        response = self.client.get('/api/schedules/', {'date': '{0}-{1}-{2}'.format(self.p_start.year, self.p_start.month, self.p_start.day),
                                                 'parking': self.parking.id})
        self.assertEqual(response.status_code, 200, msg='Bad status code')
        self.assertTrue(response.data, msg='Data segment is empty')

    def test_check_schedule_for_tomorrow(self):
        # prepare
        self.get_token()
        # do
        response = self.client.get('/api/schedules/', {'date': '{0}-{1}-{2}'.format(self.p_start.year, self.p_start.month, self.p_start.day+1),
            'parking': self.parking.id})
        # check
        self.assertEqual(response.status_code, 204, msg='Bad status code')
        self.assertFalse(response.data, msg='Data should be empty')

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
from schedule.periods import Day, Period

from datetime import timedelta

class ScheduleLotTest(TestCase):
    def setUp(self):
        self.lot = ScheduleLot.objects.create(name='Strefa A')
        self.rule = Rule.objects.create(frequency='WEEKLY', name='weekly')

        self.s1_day = timezone.make_aware(datetime(2016, 12, 26))
        self.s1_start = timezone.make_aware(datetime(2016, 12, 26, 8))
        self.s1_end = timezone.make_aware(datetime(2016, 12, 26, 17))
        self.sch1 = Schedule.objects.create(start=self.s1_start, end=self.s1_end,
                schedule_lot=self.lot, rule=self.rule)

        self.s2_day = timezone.make_aware(datetime(2016, 12, 27))
        self.s2_start = timezone.make_aware(datetime(2016, 12, 27, 8))
        self.s2_end = timezone.make_aware(datetime(2016, 12, 27, 17))
        self.sch2 = Schedule.objects.create(start=self.s2_start, end=self.s2_end,
                schedule_lot=self.lot, rule=self.rule)

        self.s3_day = timezone.make_aware(datetime(2016, 12, 28))
        self.s3_start = timezone.make_aware(datetime(2016, 12, 28, 8))
        self.s3_end = timezone.make_aware(datetime(2016, 12, 28, 17))
        self.sch3 = Schedule.objects.create(start=self.s3_start, end=self.s3_end,
                schedule_lot=self.lot, rule=self.rule)

        self.s4_day = timezone.make_aware(datetime(2016, 12, 29))
        self.s4_start = timezone.make_aware(datetime(2016, 12, 29, 8))
        self.s4_end = timezone.make_aware(datetime(2016, 12, 29, 17))
        self.sch4 = Schedule.objects.create(start=self.s4_start, end=self.s4_end,
                schedule_lot=self.lot, rule=self.rule)

        self.s5_day = timezone.make_aware(datetime(2016, 12, 30))
        self.s5_start = timezone.make_aware(datetime(2016, 12, 30, 8))
        self.s5_end = timezone.make_aware(datetime(2016, 12, 30, 17))
        self.sch5 = Schedule.objects.create(start=self.s5_start, end=self.s5_end,
                schedule_lot=self.lot, rule=self.rule)

    def test_get_related_schedules(self):
        # prepare
        # do
        schedules = self.lot.schedule_set.all()
        # check
        self.assertEqual(len(schedules), 5, msg='Wrong number of schedules')

    def test_get_schedule_from_one_day(self):
        # prepare
        t = Ticket(self.s1_start, self.s1_start + timedelta(hours=2))
        # do
        schedule = self.lot.get_schedule_for_date(t.start)
        # check
        self.assertEqual(schedule.start, self.s1_start, msg='Wrong schedule')

    def test_get_schedule_week_later(self):
        # prepare
        start = self.s1_start + timedelta(days=7)
        t = Ticket(start, start + timedelta(hours=2))
        # do
        schedule = self.lot.get_schedule_for_date(t.start)
        # check
        self.assertEqual(schedule.start, start, msg='Wrong schedule')

    def test_get_schedule_start_before_ends_in(self):
        # prepare
        t = Ticket(self.s1_start - timedelta(hours=1), self.s1_end - timedelta(hours=2))
        # do
        schedule = self.lot.get_schedule_for_date(t.start)
        # check
        self.assertEqual(schedule.start, self.s1_start, msg='Wrong schedule')

    def test_get_schedule_start_in_ends_in(self):
        # prepare
        t = Ticket(self.s1_start + timedelta(hours=2), self.s1_end - timedelta(hours=2))
        # do
        schedule = self.lot.get_schedule_for_date(t.start)
        # check
        self.assertEqual(schedule.start, self.s1_start, msg='Wrong schedule')

    def test_get_schedule_start_in_ends_after(self):
        # prepare
        t = Ticket(self.s1_start + timedelta(hours=3), self.s1_end + timedelta(hours=2))
        # do
        schedule = self.lot.get_schedule_for_date(t.start)
        # check
        self.assertEqual(schedule.start, self.s1_start, msg='Wrong schedule')

    def test_weeks_later_day(self):
        # prepare
        schedules = Schedule.objects.all()
        # do
        occur = Day(schedules, timezone.make_aware(datetime(2017, 1, 11))).get_occurrences()
        # check
        self.assertEqual(len(occur), 1, msg='Should be only one schedule in day')

    def test_weeks_later_period(self):
        # prepare
        schedules = Schedule.objects.all()
        # do
        occurs = Period(schedules, start=(self.s3_start + timedelta(weeks=4)),
                end=(self.s3_end + timedelta(weeks=4))).get_occurrences()
        self.assertEqual(len(occurs), 1, msg='Should be only one schedule')

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

