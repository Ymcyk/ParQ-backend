from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext as _
from schedule.models import Event
from ordered_model.models import OrderedModel

class ScheduleLot(models.Model):
    name = models.CharField(_('name'), 
            max_length=50
            )
    description = models.CharField(_('description'),
            max_length=150,
            blank=True
            )

    def __str__(self):
        return self.name

class Charge(models.Model):
    cost = models.DecimalField(_('cost'),
            max_digits=8,
            decimal_places=2
            )
    minutes = models.IntegerField(_('minutes'))
    duration = models.DurationField(_('duration'),
            blank=True
            )
    minute_billing = models.BooleanField(_('minutes'),
            default=True)

    def __str__(self):
        return '{}/[] for {}, minute_billing: {}'.format(self.cost, 
                self.minutes, self.duration, self.minute_billing)

    def calculate_price(self, time):
        price = Decimal()
        price += (time // self.minutes) * self.cost
        price += (Decimal(time % self.minutes) / self.minutes) * self.cost
        return price

class Schedule(Event):
    schedule_lot = models.ForeignKey(ScheduleLot,
            verbose_name=_('schedule lot'),
            on_delete=models.CASCADE
            )
    charges = models.ManyToManyField(Charge, through='ScheduleCharge')

class ScheduleCharge(OrderedModel):
    schedule = models.ForeignKey(Schedule)
    charge = models.ForeignKey(Charge)
    order_with_respect_to = 'schedule'

    class Meta:
        ordering = ('schedule', 'order')
