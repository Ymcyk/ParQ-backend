from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from schedule.models import Rule
from djroles.models import Role
from django.contrib.auth.models import User
from users.models import Driver, Officer
from .models import Parking, Ticket
from badges.models import Badge, Vehicle
from charges.models import Schedule, ScheduleLot, Charge, ScheduleCharge

from users.exceptions import NotEnoughMoney

from rest_framework.test import APIClient

class APITest(TestCase):
    def setUp(self):
        self.role = Role.objects.create_role(name='Driver')
        self.role = Role.objects.create_role(name='Officer')
        self.password = 'test'
        self.user = User.objects.create_user(username='test', password=self.password, email='test@test.com')
        self.driver = Driver.objects.create(user=self.user)
        self.client = APIClient()

    def get_token(self):
        response = self.client.post('/api/login/', {'username': self.user.username, 'password': self.password, 'role': 'driver'})
        self.token = response.data['token']

    def test_login(self):
        # prepare
        # do
        response = self.client.post('/api/login/', {'username': self.user.username, 'password': self.password, 'role': 'driver'})
        self.get_token()
        #check
        self.assertEqual(response.status_code, 200, msg='Bad code')

    def test_bad_login_credentials(self):
        # prepare
        # do
        response = self.client.post('/api/login/', {'username': self.user.username + 'x', 'password': self.password, 'role': 'driver'})
        # check
        self.assertEqual(response.status_code, 400, msg='Bad code')

    def test_register(self):
        # prepare
        # do
        response = self.client.post('/api/register/', 
                {'user': {'username': 'piotr', 'password': 'piotr', 'email': 'piotr@piotr.com'}}, format='json')
        # check
        user = User.objects.get(username='piotr')
        self.assertTrue(bool(user), msg='User not created')
        self.assertTrue(Role.has_role(user, Driver), msg='Bad user role')
        self.assertFalse(Role.has_role(user, Officer), msg='Have bad role')

class MyParkingsTest(TestCase):
    def setUp(self):
        lot = ScheduleLot.objects.create(name='Zwykły taryfikator')
        self.parking = Parking.objects.create(name='Strefa A', 
                schedule_lot=lot)

        now = timezone.now()
        self.p_start = timezone.make_aware(datetime(now.year, now.month, now.day, 0, 1))
        self.p_end = timezone.make_aware(datetime(now.year, now.month, now.day, 23, 59))

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
        
    def get_token(self):
        self.client = APIClient()
        response = self.client.post('/api/login/', {'username': self.user.username, 'password': self.password, 'role': 'driver'})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token) 

    def test_api_driver_without_tickets(self):
        # prepare
        self.get_token()
        # do
        response = self.client.get('/api/tickets/', {'parking': self.parking.id})
        # check
        self.assertFalse(response.data, msg='User have ticketes')
        self.assertEqual(response.status_code, 200, msg='Bad code')

    def test_api_driver_get_vehicles(self):
        # prepare
        self.get_token()
        # do
        response = self.client.get('/api/vehicles/')
        # check
        self.assertEqual(response.status_code, 200, msg='Bad status code')
        self.assertEqual(len(response.data), 1, msg='Bad amount of cars')

    def test_api_post_vehicle(self):
        # prepare
        self.get_token()
        # do
        response = self.client.post('/api/vehicles/', {'name': 'Maluch', 'plate_number': 'PO11111'}, formt='json')
        # check
        self.assertEqual(response.status_code, 201, msg='Bad status code')
        self.assertEqual(response.data['name'], 'Maluch', msg='Bad Vehicle name')

    def test_api_delete_vehicle(self):
        # prepare
        self.get_token()
        # do
        response = self.client.delete('/api/vehicles/{}'.format(self.vehicle.id))
        # check
        self.assertEqual(response.status_code, 204, msg='Bad status code')

    def test_api_get_parkings(self):
        # prepare
        self.get_token()
        # do
        response = self.client.get('/api/parkings/')
        # check
        self.assertEqual(response.data[0]['name'], 'Strefa A', msg='Bad parking name')

    def test_api_driver_ticket_without_money(self):
        # prepare
        self.get_token()
        start = self.p_start + timedelta(hours=1)
        end = self.p_start + timedelta(hours=2)
        # do
        response = self.client.post('/api/tickets/', {'start': start, 'end': end, 'parking': self.parking.id,
            'vehicle': self.vehicle.id})
        # check
        self.assertEqual(response.status_code, 403, msg='Bad status code')

    def test_api_driver_ticket_with_money(self):
        # prepare
        self.get_token()
        start = self.p_start + timedelta(hours=1)
        end = self.p_start + timedelta(hours=2)
        self.driver.wallet = Decimal('100.0')
        self.driver.save()
        # do
        response = self.client.post('/api/tickets/', {'start': start, 'end': end, 'parking': self.parking.id,
            'vehicle': self.vehicle.id})
        # check
        self.assertEqual(response.status_code, 201, msg='Bad status code')
        self.assertTrue(response.data, msg='No data')

    def test_api_driver_ticket_outside_schedule(self):
        # prepare
        self.get_token()
        start = self.p_start + timedelta(days=1, hours=1)
        end = self.p_start + timedelta(days=1, hours=2)
        self.driver.wallet = Decimal('100.0')
        self.driver.save()
        # do
        response = self.client.post('/api/tickets/', {'start': start, 'end': end, 'parking': self.parking.id,
            'vehicle': self.vehicle.id})
        # check
        self.assertEqual(response.status_code, 406, msg='Bad status code')
        self.assertTrue(response.data, msg='No data')

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


class ParkingsTest(TestCase):
    def setUp(self):
        lot = ScheduleLot.objects.create(name='Zwykły taryfikator')
        self.parking = Parking.objects.create(name='Strefa A', 
                schedule_lot=lot)

        now = timezone.now()
        self.p_start = timezone.make_aware(datetime(now.year, now.month, now.day, 8))
        self.p_end = timezone.make_aware(datetime(now.year, now.month, now.day, 16))

        rule = Rule.objects.create(frequency='WEEKLY', name='weekly')
        self.schedule = Schedule.objects.create(schedule_lot=lot,
                start=self.p_start, end=self.p_end, rule=rule)
        self.ch1 = Charge.objects.create(cost=1.0, minutes=60, duration=60)
        ScheduleCharge.objects.create(schedule=self.schedule, charge=self.ch1)

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

    def test_api_driver_ticket_outside_schedule(self):
        # prepare
        self.get_token()
        start = self.p_end - timedelta(hours=1)
        end = self.p_end + timedelta(hours=1)
        self.driver.wallet = Decimal('100.0')
        self.driver.save()
        # do
        response = self.client.post('/api/tickets/', {'start': start, 'end': end, 'parking': self.parking.id,
            'vehicle': self.vehicle.id})
        # check
        self.assertEqual(response.status_code, 201, msg='Bad status code')
        self.assertTrue(response.data, msg='No data')
        print(response.data)

