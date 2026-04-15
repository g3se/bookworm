from django.db.models import Q

from .models import StockBook


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
            key=lambda book: book.details.title_sortkey,
            reverse=True,
        )
    else:
        books = sorted(
            books,
            key=lambda book: book.details.title_sortkey,
        )

    return books
