from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("<int:id>/", views.book_details, name="book_details"),
    path("search/", views.search_books, name="search_books"),
]
