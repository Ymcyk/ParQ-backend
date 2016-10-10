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

    def test_badge_deactivated_after_vehicle_deletion(self):
        # prepare
        # do
        self.vehicle.delete()
        #check
        after_badge = Badge.objects.get(id=self.badge.id)
        self.assertFalse(after_badge.is_active, ('Deletion of related vehicle'
            ' did not set is_active to False'))
