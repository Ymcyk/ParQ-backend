from django.db import models
from django.contrib.auth.models import User

from .managers import ParkingUserManager

class ParkingUser(User):
    """
    Proxy User class for handling Parking user's

    Assigned to objects ParkingUserManager assign user to specific role.
    """

    objects = ParkingUserManager

    class Meta:
        proxy = True

