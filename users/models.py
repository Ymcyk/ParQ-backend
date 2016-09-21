from django.db import models
from django.contrib.auth.models import User

from .managers import ParkingUserManager

class ParkingUser(User):

    objects = ParkingUserManager

    class Meta:
        proxy = True

