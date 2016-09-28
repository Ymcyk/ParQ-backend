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
        role = self._get_role(role) if isinstance(role, str) else role
        user = super(type(self), self).create_user(*args, **kwargs)
        role.give_role(user)
        return user

    def _get_role(self, role):
        role = Role.objects.get(group__name=role)
        return role
