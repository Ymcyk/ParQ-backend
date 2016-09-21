from django.contrib.auth.models import UserManager
from .roles import *

class ParkingUserManager(UserManager):

    def create_user(self, role, *args, **kwargs):
        # przypisywanie roli
        return super(ParkingUserManager, self).create_user(*args, **kwargs)

