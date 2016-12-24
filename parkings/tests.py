from django.test import TestCase
from django.utils import timezone
import datetime

from .models import *
from badges.models import Badge

class ParkingsTest(TestCase):

    def setUp(self):
        self.p1_name = 'Strefa A'
        self.p1 = Parking.objects.create(name=self.p1_name, description='Opis')
        self.b1 = Badge.objects.create()
        self.t1 = Ticket.objects.create(badge=self.b1, parking=self.p1)

    def test_parking_created(self):
        # prepare
        # do
        # check
        self.assertTrue(bool(self.p1), msg='Parking was not created')

    def test_ticket_created(self):
        # prepare
        # do
        # check
        self.assertTrue(bool(self.t1), msg='Ticket was not created')

    def test_parking_str(self):
        # prepare
        # do
        # check
        self.assertEqual(self.p1_name, str(self.p1), 
                msg='__str__ did not returned parking name')

    def test_ticket_start_is_set(self):
        # prepare
        # do
        # check
        from datetime import datetime
        self.assertTrue(isinstance(self.t1.start, datetime), 
                msg='start is not set as datetime')

    def test_set_ticket_price(self):
        # prepare
        price = 14.96
        self.t1.price = price
        self.t1.save()
        # do
        from decimal import Decimal, ROUND_HALF_EVEN
        price = Decimal(Decimal(price).quantize(Decimal('0.00000001'), 
            ROUND_HALF_EVEN))
        t1 = Ticket.objects.get(id=self.t1.id)
        # check
        self.assertEqual(t1.price, price,
                msg='Price was not set')
