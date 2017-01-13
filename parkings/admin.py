from django.contrib import admin

from .models import Parking, Ticket

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    pass

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass
