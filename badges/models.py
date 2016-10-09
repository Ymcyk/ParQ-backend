from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from django_countries.fields import CountryField

class Vehicle(models.Model):
    """
    Driver's vehicles
    """
    DEFAULT_COUNTRY = 'PL'

    owner = models.ForeignKey(
            User,
            verbose_name=_('Vehicle\'s owner'),
            on_delete=models.CASCADE,
            # limit_choices_to={},
            )
    name = models.CharField(
            _('Name'),
            max_length=50,
            blank=True,
            )
    plate_country = CountryField(
            _('Plate country'),
            default=DEFAULT_COUNTRY,
            )
    plate_number = models.CharField(
            _('Plate number'),
            max_length=20,
            )

    def __str__(self):
        plate_str = '{}-{}'.format(self.plate_country, self.plate_number)
        return '{} {}'.format(self.name, plate_str) if self.name else plate_str 

    def __eq__(self, other):
        """
        Vehicle's are equal when plate number and country is the same
        """
        return self._is_number_eq(other) and self._is_country_eq(other)  

    def _is_number_eq(self, other):
        return self.plate_number == other.plate_number

    def _is_country_eq(self, other):
        return self.plate_country == other.plate_country
