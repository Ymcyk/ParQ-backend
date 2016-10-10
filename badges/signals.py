from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Vehicle, Badge

@receiver(post_delete, sender=Vehicle)
def deactivate_badge(sender, instance, *args, **kwargs):
    """
    After vehicle deletion, related badge is deactivated.
    """
    badge = Badge.objects.get(id=instance.badge.id)
    badge.is_active = False
    badge.save()

