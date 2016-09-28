from django.contrib.auth.models import User

class RoleUser(User):

    class Meta:
        proxy = True

