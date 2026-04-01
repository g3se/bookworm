from django.conf import settings
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.user)
    
