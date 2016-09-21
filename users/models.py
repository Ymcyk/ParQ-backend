from django.db import models
from django.contrib.auth.models import User

class ParkingUser(User):
    objects = None

    class Meta:
        proxy = True

