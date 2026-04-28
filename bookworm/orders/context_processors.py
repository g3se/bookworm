from .models import Cart, CartItem
from accounts.models import Customer

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            cart, _ = Cart.objects.get_or_create(customer=customer)
            count = sum(item.quantity for item in CartItem.objects.filter(cart=cart))
            return {'cart_item_count': count}
        except Customer.DoesNotExist:
            pass
    return {'cart_item_count': 0}