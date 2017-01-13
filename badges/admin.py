from django.contrib import admin

from .models import Vehicle, Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    pass
