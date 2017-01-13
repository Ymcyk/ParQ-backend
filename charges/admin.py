from django.contrib import admin

from ordered_model.admin import OrderedTabularInline
from charges.models import ScheduleLot, Schedule, Charge, ScheduleCharge
from schedule.models import Event, Rule, Calendar, CalendarRelation

admin.site.unregister(Event)
admin.site.unregister(Rule)
admin.site.unregister(Calendar)
admin.site.unregister(CalendarRelation)

class ScheduleChargeInline(admin.TabularInline):
    model = ScheduleCharge
    extra = 1

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    inlines = (ScheduleChargeInline,)
    ordering = ('start',)

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    inlines = (ScheduleChargeInline,)

class RuleProxy(Rule):
    class Meta:
        proxy = True
        verbose_name = 'Rule'
        verbose_name_plural = 'Rules'

admin.site.register(RuleProxy)
