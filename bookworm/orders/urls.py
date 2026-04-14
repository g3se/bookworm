from django.urls import path

from . import views


urlpatterns = [
    path("history/", views.view_order_history, name="order_history"),
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/increase/<int:item_id>/", views.increase_quantity, name="increase_quantity"),
    path("cart/decrease/<int:item_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("cart/checkout/", views.checkout, name="checkout"),
    path("cart/apply-coupon/", views.apply_coupon, name="apply_coupon"),
]
