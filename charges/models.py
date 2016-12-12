from django.db import models
from django.utils.translation import ugettext as _
from schedule.models import Event
from ordered_model.models import OrderedModel

# Trzeba się zdecydować jaki typ stosować: IntegerField, czy DuratonField
# Duration będzie dużo wygodniejszy w adminie

class Tariff(models.Model):
    cost = models.DecimalField(_('cost'),
            max_digits=8,
            decimal_places=2
            )
    minutes = models.IntegerField(_('minutes'))

    def __str__(self):
        return '{}/{}'.format(self.cost, self.minutes)

    def get_tariff_per_minute(self):
        return self.cost/self.minutes

    def calculate_cost_for_time(self, time):
        minute_tariff = self.get_tariff_per_minute()
        return minute_tariff * time

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
    tariff = models.ForeignKey(Tariff, 
            verbose_name=_('tariff')
            )
    duration = models.DurationField(_('duration'),
            blank=True
            )
    minute_billing = models.BooleanField(_('minutes'),
            default=True)

    def __str__(self):
        return '{} for {}, minute_billing: {}'.format(self.tariff, 
                self.duration, self.minute_billing)

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
