from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("<int:id>/", views.book_details, name="book_details"),
]
