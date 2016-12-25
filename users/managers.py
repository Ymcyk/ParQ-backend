from django.contrib.auth.models import UserManager

from djroles.models import Role

class RoleUserManager(UserManager):
    """
    Custom RoleUser manager.
    Responsible for assigning users to specific role.
    """
    def assign_to_role(self, role_class, user):
        role = Role.objects.get_for_class(role_class)
        role.give_role(user)

    def create_role_user(self, role, *args, **kwargs):
        """
        Create user and give him role
        """
        user = super(type(self), self).create_user(*args, **kwargs)
        self.assign_to_role(role, user)
        return user

