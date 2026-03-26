from django.db import models


class Cart(models.Model):
    """Current cart of a Customer before the order has been placed."""

    customer = models.OneToOneField("accounts.Customer", on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # index as an element of the cart's "list"
    # NOTE: It may be useful to not assume that all CartItems in a Cart have
    #       contiguous indices to make it easier to implement the ability to
    #       delete items in a cart.
    index = models.PositiveIntegerField()
    book = models.ForeignKey("catalog.StockBook", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    """Order placed by a Customer.
    May or may not have been fulfilled.

    These may be kept indefinitely for the company's records, so they need to
    resist change/deletion from other parts of the software's model.
    """

    customer = models.ForeignKey("accounts.Customer", on_delete=models.SET_NULL, null=True)
    # auto_now_add automatically sets created_at to the datetime at the
    # creation of the Order
    created_at = models.DateTimeField(auto_now_add=True)
    # NOTE: total_price is *probably* large enough.
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_fulfilled = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey("catalog.BookDetails", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    # NOTE: price_at_purchase should have the same precision as price of
    #       StockBook.
    # TODO: Should this be `price_of_book * quantity` or just `price_of_book`?
    price_at_purchase = models.DecimalField(max_digits=6, decimal_places=2)
