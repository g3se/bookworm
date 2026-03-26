from django.db import models


class BookDetails(models.Model):
    """Book details, independent of stock.

    Preferably, these should never be deleted.
    """

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Book details"
        verbose_name_plural = "Book details"


class StockBook(models.Model):
    """Copies of a book as a part of the store's stock."""

    details = models.OneToOneField(BookDetails, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"(x{self.stock}) {self.details}"

    class Meta:
        verbose_name = "Book in stock"
        verbose_name_plural = "Books in stock"
