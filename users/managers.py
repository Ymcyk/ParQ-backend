from django.contrib.auth.models import UserManager

from djroles.models import Role

class RoleUserManager(UserManager):
    """
    Custom RoleUser manager.
    Responsible for assigning users to specific role.
    """

    def create_user_with_role(self, role, *args, **kwargs):
        """
        Create user and give him role
        """
        if isinstance(role, str):
            role = self._get_role(role)
        elif not isinstance(role, Role):
            raise TypeError('Unkown type {} given at role argument'.
                    format(type(role)))
        user = super(type(self), self).create_user(*args, **kwargs)
        role.give_role(user)
        return user

    def _get_role(self, role):
        role = Role.objects.get(group__name=role)
        return role
