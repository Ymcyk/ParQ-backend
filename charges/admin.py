from django.contrib import admin
from ordered_model.admin import OrderedTabularInline
from .models import Schedule, ScheduleCharge

class ScheduleChargeInline(OrderedTabularInline):
    model = ScheduleCharge
    fields = ('charge', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'mocve_up_down_links',)
    extra = 1
    ordering = ('order',)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = (ScheduleChargeInline,)
    
    def get_urls(self):
        urls = super(type(self), self).get_urls()
        for inline in self.ilines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls

admin.site.register(Schedule, ScheduleAdmin)

