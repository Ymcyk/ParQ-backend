from django.test import TestCase
from django.contrib.auth.models import User

from django.db import IntegrityError

from djroles.models import Role
from users.models import Driver
from .models import Badge, Vehicle

class VehicleTest(TestCase):
    def setUp(self):
        self.username = 'jan'
        Role.objects.create_role(name='Driver')
        self.user = User.objects.create_user(username=self.username)
        self.driver = Driver.objects.create(user=self.user)
        self.badge = Badge.objects.create()
        self.vehicle = Vehicle.objects.create(owner=self.driver, badge=self.badge,
                plate_number='ZS123FU')

    def test_badge_is_created(self):
        # prepare
        # do
        # check
        self.assertIsNotNone(self.badge, msg=('Badge not created'))

    def test_vehicle_created_with_given_badge(self):
        # prepare
        ret_badge = self.vehicle.badge
        # do
        # check
        self.assertEqual(self.badge, ret_badge, msg='Vehicle with another ' 
                'badge')

    def test_badge_unassigned_on_create(self):
        '''
        is_assigned should be False (not assigned) on create.
        '''
        # prepare
        # do
        badge = Badge.objects.create()
        # check
        self.assertFalse(badge.is_assigned, msg='Badge assigned on create.')

    def test_badge_assigned_after_vehicle_save(self):
        '''
        is_assigned set to True after vehicle save
        '''
        # prepare
        # do
        # check
        after_badge = Badge.objects.get(id=self.badge.id)
        self.assertTrue(after_badge.is_assigned, ('Badge after vehicle save'
            ' not changed to True'))

    def test_cant_assign_to_assigned_badge(self):
        # prepare
        # do
        # check
        from badges.exceptions import BadgeNotAvailable
        with self.assertRaises(IntegrityError, msg=('Asigning vehicle to'
            ' assigned badge didn\'t raise Error')):
            Vehicle.objects.create(owner=self.driver, badge=self.badge,
                    plate_country='PL', plate_number='ZS1234F')

    def test_badge_deleted_after_vehicle_deletion(self):
        '''
        After vehicle delete in post_delete signal badge should be deleted
        '''
        # prepare
        # do
        self.vehicle.delete()
        # check
        with self.assertRaises(Badge.DoesNotExist, msg=('Badge exist after' 
                'Vehicle deletion')):
            Badge.objects.get(pk=self.badge.pk)

    def test_cant_assign_after_vehicle_delete(self):
        '''
        Badge can be used only once. Even after related vehicle delete can't
        be reused.
        '''
        # prepare
        # do
        self.vehicle.delete()
        # check
        with self.assertRaises(ValueError, msg=('Can assign after'
            ' vehicle deletion')):
            Vehicle.objects.create(owner=self.user, badge=self.badge,
                    plate_country='PL', plate_number='ZS1234F')

