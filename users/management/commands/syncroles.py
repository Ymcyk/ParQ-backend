from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission
from importlib import import_module
from inspect import getmembers, isclass

from djroles.models import Role
from djroles.exceptions import RoleError

class Command(BaseCommand):
    """
    Add new roles from roles.py module.
    Replaces all role permissions in db with specified in roles module.
    """
    help = ('Look for BaseRole derived classes in users.roles.py. syncrules'
            ' command to start.')

    def handle(self, *args, **options):
        module_values = self._get_role_values('users.models')
        new_roles = self._sync_roles(module_values)
        # [print(role) for role in new_roles]
        print(module_values)

    def _sync_roles(self, module_roles):
        new_roles = []
        for role_name in module_roles.keys():
            try:
                role = Role.objects.create_role(name=role_name)
            except RoleError:
                continue
            new_roles.append(role)
        return new_roles

    # nie będzie tworzyć nowych uprawnień. Jeśli podane w pliku nie istnieje,
    # to się wywala
    def _assign_permissions(self, role, perms_names):
        permissions = [Permission.objects.get(codename=perm) 
                for perm in perms_names]

    def _get_role_values(self, module):
        roles = import_module(module)
        return {
                role_class[0]: getattr(role_class[1], 'permissions', ()) 
                for role_class in getmembers(roles, isclass)
                if role_class[1].__module__ == roles.__name__ and
                   issubclass(role_class[1], roles.BaseRole)
        }

