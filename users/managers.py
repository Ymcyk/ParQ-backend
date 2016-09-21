from django.contrib.auth.models import UserManager
from .roles import *

class ParkingUserManager(UserManager):
    """
    Custom ParkingUser manager.
    Responsible for assigning users to specific role.
    """

    def create_user(self, role, *args, **kwargs):
        # przypisywanie roli
        return super(ParkingUserManager, self).create_user(*args, **kwargs)

