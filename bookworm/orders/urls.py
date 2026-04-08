from django.urls import path

from . import views


urlpatterns = [
    path("history/", views.view_order_history, name="order_history"),
]
