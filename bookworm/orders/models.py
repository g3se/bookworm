from django.db import models


class Cart(models.Model):
    """Current cart of a Customer before the order has been placed."""

    customer = models.OneToOneField(
        "accounts.Customer", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.customer)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey("catalog.StockBook", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cart.customer}: (x{self.quantity}) {self.book.details}"


class Order(models.Model):
    """Order placed by a Customer.
    May or may not have been fulfilled.

    These may be kept indefinitely for the company's records, so they need to
    resist change/deletion from other parts of the software's model.
    """

    customer = models.ForeignKey(
        "accounts.Customer", on_delete=models.SET_NULL, null=True
    )
    # auto_now_add automatically sets created_at to the datetime at the
    # creation of the Order
    created_at = models.DateTimeField(auto_now_add=True)
    # NOTE: total_price is *probably* large enough.
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_fulfilled = models.BooleanField(default=False)

    def __str__(self):
        customer_str = str(self.customer) if self.customer else "[Deleted Customer]"
        return f"{customer_str} ({self.created_at})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(
        "catalog.BookDetails", on_delete=models.SET_NULL, null=True
    )
    quantity = models.PositiveIntegerField()
    # NOTE: price_at_purchase should have the same precision as price of
    #       StockBook.
    # TODO: Should this be `price_of_book * quantity` or just `price_of_book`?
    price_at_purchase = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        customer_str = str(self.order.customer) if self.order.customer else "[Deleted Customer]"
        book_str = str(self.book) if self.book else "[Deleted Book]"
        return f"{customer_str}: (x{self.quantity}) {book_str}"
