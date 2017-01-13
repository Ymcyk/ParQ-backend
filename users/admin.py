from django.contrib import admin

from .models import Driver, Officer
from badges.models import Vehicle

class VehicleInline(admin.TabularInline):
    model = Vehicle

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    inlines = [
        VehicleInline,        
    ]

@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    pass
