from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Vehicle

@receiver(post_delete, sender=Vehicle)
def delete_related_badge(instance, **kwargs):
    instance.badge.delete()
