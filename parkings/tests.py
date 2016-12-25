from django.test import TestCase
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from decimal import Decimal

from schedule.models import Rule
from djroles.models import Role
from django.contrib.auth.models import User
from users.models import Driver
from .models import Parking, Ticket
from badges.models import Badge, Vehicle
from charges.models import Schedule, ScheduleLot, Charge, ScheduleCharge

from users.exceptions import NotEnoughMoney

class ParkingsTest(TestCase):
    def setUp(self):
        lot = ScheduleLot.objects.create(name='Zwykły taryfikator')
        self.parking = Parking.objects.create(name='Strefa A', 
                schedule_lot=lot)

        self.p_start = make_aware(datetime(2016, 12, 24, 8))
        self.p_end = make_aware(datetime(2016, 12, 24, 17))
        rule = Rule.objects.create(frequency='WEEKLY', name='weekly')
        self.schedule = Schedule.objects.create(schedule_lot=lot,
                start=self.p_start, end=self.p_end, rule=rule)
        self.ch1 = Charge.objects.create(cost=.7, minutes=15, duration=15, minute_billing=False)
        ScheduleCharge.objects.create(schedule=self.schedule, charge=self.ch1)
        self.ch2 = Charge.objects.create(cost=2.8, minutes=60, duration=60)
        ScheduleCharge.objects.create(schedule=self.schedule, charge=self.ch2)
        self.ch3 = Charge.objects.create(cost=3.2, minutes=60, duration=60)
        ScheduleCharge.objects.create(schedule=self.schedule, charge=self.ch3)

        user = User.objects.create_user(username='Jan')
        role = Role.objects.create_role(name='Driver')
        self.driver = Driver.objects.create(user=user)
        badge = Badge.objects.create()
        self.vehicle = Vehicle.objects.create(owner=self.driver, badge=badge,
                plate_number='ZS12345', plate_country='PL', name='Golf')

    def test_parking_str(self):
        # prepare
        # do
        # check
        self.assertEqual(str(self.parking), 'Strefa A', msg='__str__')

    def test_driver_without_money(self):
        # prepare
        # do
        # check
        with self.assertRaises(NotEnoughMoney, msg='Exception not raised'):
            t = Ticket.objects.create(vehicle=self.vehicle, parking=self.parking,
                    start=self.p_start, end=self.p_start + timedelta(hours=1))

    def test_driver_money_reduced(self):
        # prepare
        money = Decimal('10.0')
        self.driver.add_money(money)
        self.driver.save()
        # do
        t = Ticket.objects.create(vehicle=self.vehicle, parking=self.parking,
                start=self.p_start + timedelta(hours=1),
                end=self.p_start + timedelta(hours=3, minutes=15))
        # check
        driver = Driver.objects.get()
        self.assertEqual(driver.wallet, Decimal('3.3'), msg='Wallet amount')
