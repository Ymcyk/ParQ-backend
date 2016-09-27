from django.contrib.auth.models import User

from .managers import RoleUserManager

class RoleUser(User):
    objects = RoleUserManager()

    class Meta:
        proxy = True

