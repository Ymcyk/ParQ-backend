from django.test import TestCase
from django.contrib.auth.models import Group
from djroles.models import Role

from .models import Driver, Officer

class UsersTest(TestCase):

    def setUp(self):
        self.officer_group = Role.objects.create_role(name='Officer')
        self.driver_group = Role.objects.create_role(name='Driver')

    def test_officer_is_created(self):
        # prepare
        officer = Officer.objects.create_user(username='test_user')
        # do
        group = Role.objects.get_user_role(officer)
        # check
        self.assertTrue(group == self.officer_group, 
                msg='Officer with bad group')

    #def test_driver_is_created(self):
    #    # prepare
    #    driver = Driver.objects.create_user(username='test_user')
    #    # do
    #    group = Role.objects.get_user_role(driver)
    #    # check
    #    self.assertTrue(group == self.driver_group, 
    #            msg='Driver with bad group')

