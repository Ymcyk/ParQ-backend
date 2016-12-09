from django.contrib.auth.models import User
from djroles.models import Role
from djroles.roles import BaseRole

class Officer(User, BaseRole):
    class Meta:
        proxy = True

class Driver(User, BaseRole):
    class Meta:
        proxy = True

