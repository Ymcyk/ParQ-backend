from django.db import models

from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            )
    transaction_id = models.CharField(
            max_length=28,
            unique=True,
            )

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.transaction_id)

