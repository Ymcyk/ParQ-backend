from django.test import TestCase
from .models import Charge

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

