from django.test import TestCase
from django.contrib.auth.models import Group, User
from djroles.models import Role
from rest_framework.authtoken.models import Token

from .models import Driver, Officer

class UsersTest(TestCase):

    def setUp(self):
        self.officer_group = Role.objects.create_role(name='Officer')
        self.driver_group = Role.objects.create_role(name='Driver')
        self.user = User.objects.create_user(username='test', 
                password='piotr213243', email='test@test.pl')

    def test_officer_is_created(self):
        # prepare
        officer = Officer.objects.create(user=self.user)
        # do
        group = Role.objects.get_user_role(officer.user)
        token = Token.objects.get()
        # check
        self.assertTrue(group == self.officer_group, 
                msg='Officer with bad group')
        self.assertEqual(token.user, officer.user, msg='Bad token')

    def test_driver_is_created(self):
        # prepare
        driver = Driver.objects.create(user=self.user)
        # do
        group = Role.objects.get_user_role(driver.user)
        token = Token.objects.get()
        # check
        self.assertTrue(group == self.driver_group, msg='Bad group')
        self.assertEqual(token.user, driver.user, msg='Bad token')


