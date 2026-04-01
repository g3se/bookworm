from django.db import models
from django.utils.html import mark_safe

from bookworm.settings import MEDIA_URL

GENRE_CHOICES = [
    ("fiction", "Fiction"),
    ("history", "History"),
    ("sci-fi", "Sci-Fi"),
    ("biography", "Biography"),
    ("romance", "Romance"),
    ("fantasy", "Fantasy"),
    ("mystery", "Mystery"),
    ("thriller", "Thriller"),
    ("non-fiction", "Non-Fiction"),
    ("dystopian", "Dystopian"),
]

class BookDetails(models.Model):
    """Book details, independent of stock.

    Preferably, these should never be deleted.
    """

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    genre = models.CharField(max_length=127, choices=GENRE_CHOICES)
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

    def __str__(self):
        return f"(x{self.stock}) {self.details}"

    class Meta:
        verbose_name = "Book in stock"
        verbose_name_plural = "Books in stock"
