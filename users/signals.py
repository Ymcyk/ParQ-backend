from django.db.models.signals import post_save
from django.dispatch import receiver
from djroles.models import Role

from .models import Driver, Officer

def assign_to_role(role_class, user):
    role = Role.objects.get_for_class(role_class)
    role.give_role(user)

@receiver(post_save, sender=Driver)
def assign_driver_to_group(instance, created, **kwargs):
    if created:
        assign_to_role(Driver, instance)

@receiver(post_save, sender=Officer)
def assign_officer_to_group(instance, created, **kwargs):
    if created:
        assign_to_role(Officer, instance)
