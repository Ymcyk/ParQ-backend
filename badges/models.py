import os

import uuid
import qrcode

from django.conf import settings
from django.db import models, IntegrityError
from django.utils.translation import ugettext as _
from users.models import Driver
from django_countries.fields import CountryField

from .exceptions import BadgeNotAvailable

class Badge(models.Model):
    """
    Badge with auto generated uuid
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    @property
    def is_assigned(self):
        return hasattr(self, 'vehicle')

    def path_to_file(self):
        path = os.path.join(settings.BASE_DIR, 'badges', 'images')
        return '{0}/{1}.png'.format(path, self.uuid)

    def generate_image(self):
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=20,
            border=4
            )
        qr.add_data(self.uuid)
        path = os.path.join(settings.BASE_DIR, 'badges', 'images')
        return qr.make_image().save(self.path_to_file())

    def save(self, *args, **kwargs):
        super(type(self), self).save(*args, **kwargs)
        self.generate_image()

    def __str__(self):
        return '{0}, uuid: {1}'.format(self.id, self.uuid)

class Vehicle(models.Model):
    """
    Driver's vehicles
    """
    DEFAULT_COUNTRY = 'PL'

    owner = models.ForeignKey(
            Driver,
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

