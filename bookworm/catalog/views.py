from django.shortcuts import render, get_object_or_404
from .models import StockBook


def book_list(request):
    books = StockBook.objects.all()

    return render(request, "catalog/book_list.html", {"books": books})


def book_details(request, id):
    book = get_object_or_404(StockBook, id=id)

    return render(request, "catalog/book_details.html", {"book": book})
