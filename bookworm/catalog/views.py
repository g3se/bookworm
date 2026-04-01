from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import StockBook, BookDetails

def search_books(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        results = BookDetails.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query) |
            Q(genre__icontains=query)
        )

    return render(request, "catalog/search_results.html", {"results": results, "query": query})

def book_list(request):
    books = StockBook.objects.all()

    return render(request, "catalog/book_list.html", {"books": books})


def book_details(request, id):
    book = get_object_or_404(StockBook, id=id)

    return render(request, "catalog/book_details.html", {"book": book})
