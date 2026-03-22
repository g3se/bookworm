from django.db import models


class BookDetails(models.Model):
    """Book details, independent of stock.

    Preferably, these should never be deleted.
    """

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)


class StockBook(models.Model):
    """Copies of a book as a part of the store's stock."""

    details = models.OneToOneField(BookDetails, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
