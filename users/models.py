from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from djroles.models import Role
from djroles.roles import BaseRole
from django.utils.translation import ugettext as _

from .exceptions import NotEnoughMoney

class Officer(models.Model, BaseRole):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True
            )
    position = models.CharField(
            _('position'),
            max_length=50,
            blank=True
            )

    def __str__(self):
        return str(self.user)

class Driver(models.Model, BaseRole):
    user = models.OneToOneField(
            User, 
            on_delete=models.CASCADE,
            primary_key=True
            )
    wallet = models.DecimalField(
            _('wallet'),
            max_digits=8,
            decimal_places=2,
            default=Decimal()
            )

    def reduce_money(self, amount):
        if self.wallet < amount:
            raise NotEnoughMoney('Driver do not have enough money')
        self.wallet -= amount

    def add_money(self, amount):
        self.wallet += amount

    def __str__(self):
        return str(self.user)

