from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from badges.models import Vehicle

from charges.models import ScheduleLot
from charges.exceptions import PeriodWithoutSchedule

class Parking(models.Model):
    name = models.CharField(
            _('name'),
            max_length=50,
            )
    description = models.CharField(
            _('description'),
            max_length=150,
            blank=True
            )
    # w przyszłości do zmiany na ManyToMany
    # ale to jak w ScheduleLot znajdzie się data obowiązywania
    schedule_lot = models.OneToOneField(ScheduleLot)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    start = models.DateTimeField(
            _('start'),
            default=timezone.now
            )
    end = models.DateTimeField(
            _('end'),
            # blank=True,
            # null=True
            )
    vehicle = models.ForeignKey(Vehicle)
    parking = models.ForeignKey('Parking')
    price = models.DecimalField(
            _('price'),
            max_digits=8,
            decimal_places=2,
            blank=True,
            null=True
            )
    # można sprawdzać jeszcze, czy data w bilecie dotyczy tego samego dnia,
    # chociaż problemem nie jest dzień, a grafik
    def save(self, *args, **kwargs):
        self.price = self.parking.schedule_lot.calculate_price(self)
        self.vehicle.owner.reduce_money(self.price)

        super(type(self), self).save(*args, **kwargs)
        self.vehicle.owner.save()

    def __str__(self):
        return '{}: {}'.format(self.start, self.parking)

