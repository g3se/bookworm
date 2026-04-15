import re

from django.db.models import Q

from .models import StockBook


ARTICLE_RE = re.compile(r"^(a|an|the)\s+", re.IGNORECASE)


def normalize_title_for_sort(title):
    return ARTICLE_RE.sub("", title).strip().lower()


def filter_and_sort_books(query, sort):
    books = StockBook.objects.select_related("details").all()

    if query:
        books = books.filter(
            Q(details__title__icontains=query)
            | Q(details__author__icontains=query)
            | Q(details__genre__icontains=query)
        )

    if sort == "price_asc":
        books = books.order_by("price")
    elif sort == "price_desc":
        books = books.order_by("-price")
    elif sort == "stock_asc":
        books = books.order_by("stock")
    elif sort == "stock_desc":
        books = books.order_by("-stock")
    elif sort == "title_desc":
        books = sorted(
            books,
            key=lambda book: normalize_title_for_sort(book.details.title),
            reverse=True,
        )
    else:
        books = sorted(
            books,
            key=lambda book: normalize_title_for_sort(book.details.title),
        )

    return books
