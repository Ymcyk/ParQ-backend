import uuid
from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from django_countries.fields import CountryField

from .exceptions import BadgeNotAvailable

class Badge(models.Model):
    """
    Randomly generated unique ID.
    """
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    @property
    def is_assigned(self):
        return hasattr(self, 'vehicle')

    def __str__(self):
        return str(self.id)

class Vehicle(models.Model):
    """
    Driver's vehicles
    """
    DEFAULT_COUNTRY = 'PL'

    owner = models.ForeignKey(
            User,
            verbose_name=_('Vehicle\'s owner'),
            on_delete=models.CASCADE,
            editable=False,
            # limit_choices_to={},
            )
    badge = models.OneToOneField(
            'Badge',
            verbose_name=_('badge'),
            editable=False,
            on_delete=models.CASCADE,
            )
    name = models.CharField(
            _('Name'),
            max_length=50,
            blank=True,
            )
    plate_country = CountryField(
            _('Plate country'),
            default=DEFAULT_COUNTRY,
            editable=False,
            )
    plate_number = models.CharField(
            _('Plate number'),
            max_length=20,
            editable=False,
            )

    def save(self, *args, **kwargs):
        try:
            super(Vehicle, self).save(*args, **kwargs)
        except IntegrityError:
            raise BadgeNotAvailable('This badge is already assigned')
        
    def __str__(self):
        plate_str = '{}-{}'.format(self.plate_country, self.plate_number)
        return '{} {}'.format(self.name, plate_str) if self.name else plate_str 

    def __eq__(self, other):
        """
        Vehicle's are equal when plate number and country are the same
        """
        return self._is_number_eq(other) and self._is_country_eq(other)  

    def _is_number_eq(self, other):
        return self.plate_number == other.plate_number

    def _is_country_eq(self, other):
        return self.plate_country == other.plate_country

