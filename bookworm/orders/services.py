from accounts.models import Customer
from catalog.models import StockBook
from django.core.exceptions import ObjectDoesNotExist

from .models import Cart, CartItem


class NotFoundError(Exception):
    pass


def add_book_to_cart(user, book_id):
    # Get the Customer profile linked to the logged in user
    try:
        customer = Customer.objects.get(user=user)
        book = StockBook.objects.get(id=book_id)
    except ObjectDoesNotExist as e:
        raise NotFoundError() from e

    # Get existing cart or create a new one for this customer
    cart, _ = Cart.objects.get_or_create(customer=customer)

    # if this book is already in the cart, increment quantity
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, book=book, defaults={"quantity": 1}
    )
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
