from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import StockBook


def book_list(request):
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "").strip()

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
    else:
        books = books.order_by("details__title")

    context = {
        "books": books,
        "query": query,
        "sort": sort,
    }

    return render(request, "catalog/book_list.html", context)


def book_details(request, id):
    book = get_object_or_404(StockBook, id=id)
    return render(request, "catalog/book_details.html", {"book": book})
