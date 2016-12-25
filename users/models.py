from django.contrib.auth.models import User
from djroles.models import Role
from djroles.roles import BaseRole
from django.utils.translation import ugettext as _

from .exceptions import NotEnoughMoney

class Officer(User, BaseRole):
    class Meta:
        proxy = True

class Driver(User, BaseRole):
    class Meta:
        proxy = True

#class Driver(models.Model, BaseRole):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    wallet = models.DecimalField(
#            _('wallet'),
#            max_digits=8,
#            decimal_places=2,
#            default=0.0
#            )
#
#    def reduce_money(self, amount):
#        if self.wallet < amount:
#            raise NotEnoughMoney('Driver do not have enough money')
#        self.wallet -= amount

#    def add_money(self, aomunt):
#        self.wallet += amount
