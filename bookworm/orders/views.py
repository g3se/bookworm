from accounts.models import Customer
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from . import services
from .models import Cart, CartItem


# Create your views here.
@login_required
def add_to_cart(request, book_id):
    try:
        services.add_book_to_cart(request.user, book_id)
    except services.NotFoundError:
        raise Http404()

    # Redirect back to whatever page they came from
    return redirect(request.META.get("HTTP_REFERER", "/"))


# TODO finish
# TODO this should probably be moved into `services.py` once completed
@login_required
def view_cart(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total for all items in the cart
    subtotal = sum(item.book.price * item.quantity for item in cart_items)


@login_required
def view_order_history(request):
    orders = services.list_order_history(request.user)
    return render(request, "accounts/order_history.html", {"orders": orders})
