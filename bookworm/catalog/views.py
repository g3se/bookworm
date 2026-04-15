from django.shortcuts import get_object_or_404, render

from . import services
from .models import StockBook


def book_list(request):
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "").strip()

    books = services.filter_and_sort_books(query, sort)

    context = {
        "books": books,
        "query": query,
        "sort": sort,
    }

    return render(request, "catalog/book_list.html", context)


def book_details(request, id):
    book = get_object_or_404(StockBook, id=id)
    return render(request, "catalog/book_details.html", {"book": book})
