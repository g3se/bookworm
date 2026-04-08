from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Cart, CartItem
from accounts.models import Customer
from catalog.models import StockBook


# Create your views here.
@login_required
def add_to_cart(request, book_id):
    # Get the Customer profile linked to the logged in user
    customer = get_object_or_404(Customer, user=request.user)
    book = get_object_or_404(StockBook, id=book_id)

    # Get existing cart or create a new one for this customer
    cart, _ = Cart.objects.get_or_create(customer=customer)

    # if this book is already in the cart, increment quantity
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, book=book, defaults={"quantity": 1}
    )
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    # Redirect back to whatever page they came from
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def view_cart(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total for all items in the cart
    subtotal = sum(item.book.price * item.quantity for item in cart_items)
