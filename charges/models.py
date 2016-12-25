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
    duration = models.IntegerField(_('duration'),
            blank=True
            )
    minute_billing = models.BooleanField(_('minutes'),
            default=True)

    def __str__(self):
        return '{}/{} for {}, minute_billing: {}'.format(self.cost, 
                self.minutes, self.duration, self.minute_billing)

    def calculate_price(self, time):
        price = Decimal()
        price += Decimal(time // self.minutes) * self.cost
        rest = (Decimal(time % self.minutes) / self.minutes) * self.cost
        if not self.minute_billing and rest:
            price += self.cost
        else:
            price += rest
        return price

class Schedule(Event):
    schedule_lot = models.ForeignKey(ScheduleLot,
            verbose_name=_('schedule lot'),
            on_delete=models.CASCADE
            )
    charges = models.ManyToManyField(Charge, through='ScheduleCharge')

    def calculate_price(self, ticket):
        effective_dates = self._get_effective_dates(ticket)
        time = self._to_minutes(effective_dates[1] - effective_dates[0])
        charges = list(self.charges.all().order_by('-schedulecharge__order'))

        if not charges:
            raise Exception('Schedule without charges')

        price = Decimal()
        while time > 0:
            charge = charges.pop()
            if len(charges) == 0 or time <= charge.duration:
                price += charge.calculate_price(time)
                break
            else:
                price += charge.calculate_price(charge.duration)
                time -= charge.duration
        return price

    def _get_effective_dates(self, ticket):
        if ticket.start > self.end or ticket.end < self.start:
            raise Exception('Ticket is not in Schedule')
        start = self.start if self.start > ticket.start else ticket.start
        end = self.end if self.end < ticket.end else ticket.end
        return (start, end)

    def _to_minutes(self, time):
        minutes = time.days * 24 * 60
        minutes += time.seconds // 60
        return minutes

class ScheduleCharge(OrderedModel):
    schedule = models.ForeignKey(Schedule)
    charge = models.ForeignKey(Charge)
    order_with_respect_to = 'schedule'

    class Meta:
        ordering = ('schedule', 'order')
