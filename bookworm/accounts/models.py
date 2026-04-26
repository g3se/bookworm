from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    @property
    def full_name(self):
        return " ".join(
            [
                name
                for name in [self.first_name, self.last_name]
                if name.strip() != ""
            ]
        )


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.user)
