from decimal import ROUND_CEILING, Decimal

from bookworm.settings import MEDIA_URL
from django.db import models
from django.utils.html import mark_safe


class BookDetails(models.Model):
    """Book details, independent of stock.

    Preferably, these should never be deleted.
    """

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    genre = models.CharField(max_length=127)
    cover_img = models.ImageField(
        upload_to="book_covers/", blank=True, null=True
    )

    def __str__(self):
        return str(self.title)

    @property
    def cover_url(self):
        if self.cover_img:
            return self.cover_img.url
        return MEDIA_URL + "placeholder.jpg"

    @property
    def description_html(self):
        return mark_safe(self.description)

    class Meta:
        verbose_name = "Book details"
        verbose_name_plural = "Book details"


class StockBook(models.Model):
    """Copies of a book as a part of the store's stock."""

    details = models.OneToOneField(BookDetails, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    original_price = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"(x{self.stock}) {self.details}"

    @property
    def is_discounted(self):
        return (
            self.original_price is not None and self.price < self.original_price
        )

    @property
    def discount_percent(self):
        if self.original_price is None:
            return Decimal("0")
        rate = Decimal("1") - (self.price / self.original_price)
        return (Decimal("100") * rate).to_integral_value(rounding=ROUND_CEILING)

    @property
    def discount_amount(self):
        if self.original_price is None:
            return Decimal("0")
        return self.original_price - self.price

    class Meta:
        verbose_name = "Book in stock"
        verbose_name_plural = "Books in stock"
