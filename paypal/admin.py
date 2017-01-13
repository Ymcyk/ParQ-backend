from django.contrib import admin

from .models import Transaction

@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    pass
