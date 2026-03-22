from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator

from accounts.models import Customer


class Coupon(models.Model):
    code = models.CharField(max_length=31, unique=True)
    is_active = models.BooleanField(default=True)
    discount_percent = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )
    used_by = models.ManyToManyField(Customer, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(discount_percent__gte=0)
                & Q(discount_percent__lte=100),
                name="discount_percent_inrange_0_to_100",
            )
        ]
