from django.test import TestCase
from django.contrib.auth.models import User

from .models import Badge, Vehicle

class VehicleTest(TestCase):
    def setUp(self):
        self.username = 'jan'
        self.user = User.objects.create_user(username=self.username)
        self.badge = Badge.objects.create()
        self.vehicle = Vehicle.objects.create(owner=self.user, badge=self.badge,
                plate_country='PL', plate_number='ZS123FU')

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

    def test_badge_deactivated_after_vehicle_deletion(self):
        '''
        Deleting related vehicle should unset is_active in Badge object
        '''
        # prepare
        # do
        self.vehicle.delete()
        #check
        after_badge = Badge.objects.get(id=self.badge.id)
        self.assertFalse(after_badge.is_active, ('Deletion of related vehicle'
            ' did not set is_active to False'))

    def test_badge_cant_have_many_vehicles(self):
        '''
        Assigned badge can't be assigned to other vehicle
        '''
        # prepare
        # do
        # check
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError, msg=('Second vehicle didn\'t' 
            ' rise Error')):
            vehicle2 = Vehicle.objects.create(owner=self.user, badge=self.badge, 
                       plate_country='PL', plate_number='PO123FU')

    def test_cant_assign_to_deactivated_badge(self):
        # prepare
        # do
        # check
        pass

