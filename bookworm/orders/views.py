from decimal import Decimal

from accounts.models import Customer
from coupons.models import Coupon
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from . import services
from .models import Cart, CartItem, Order, OrderItem

TAX_RATE = Decimal("0.0825")  # 8.25% Texas sales tax


@login_required
def add_to_cart(request, book_id):
    try:
        services.add_book_to_cart(request.user, book_id)
    except services.NotFoundError:
        raise Http404()
    # There are two places where the Add to Cart button is available,
    # and this redirect makes sense for both.
    return redirect("catalog:book_list")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("view_cart")


@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect("view_cart")


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect("view_cart")


@login_required
def view_cart(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart).select_related(
        "book__details"
    )

    subtotal = sum(item.book.price * item.quantity for item in cart_items)

    # Get coupon from session if applied
    discount = Decimal("0.00")
    coupon = None
    coupon_code = request.session.get("coupon_code")
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            discount = (
                subtotal * Decimal(coupon.discount_percent) / Decimal("100")
            )
        except Coupon.DoesNotExist:
            request.session.pop("coupon_code", None)

    tax = subtotal * TAX_RATE
    total = subtotal + tax - discount

    return render(
        request,
        "orders/cart.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "tax": tax,
            "discount": discount,
            "total": total,
            "coupon": coupon,
        },
    )


@login_required
def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get("coupon_code", "").strip().upper()
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            request.session["coupon_code"] = coupon.code
            messages.success(
                request,
                f"Coupon '{code}' applied! {coupon.discount_percent}% off.",
            )
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid or inactive coupon code.")
    return redirect("view_cart")


@login_required
def checkout(request):
    if request.method == "POST":
        customer = get_object_or_404(Customer, user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=customer)
        cart_items = CartItem.objects.filter(cart=cart).select_related(
            "book__details"
        )

        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect("view_cart")

        if not customer.address:
            messages.error(
                request, "Please add a delivery address before checking out."
            )
            return redirect("edit_address")

        subtotal = sum(item.book.price * item.quantity for item in cart_items)

        # Apply coupon if present
        discount = Decimal("0.00")
        coupon_code = request.session.get("coupon_code")
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                discount = (
                    subtotal * Decimal(coupon.discount_percent) / Decimal("100")
                )
                coupon.used_by.add(customer)
            except Coupon.DoesNotExist:
                pass

        tax = subtotal * TAX_RATE
        total = subtotal + tax - discount

        # Create the order
        order = Order.objects.create(
            customer=customer,
            total_price=total,
            customer_address=customer.address,
        )

        # Create order items and reduce stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book.details,
                quantity=item.quantity,
                price_at_purchase=item.book.price,
            )
            item.book.stock -= item.quantity
            item.book.save()

        # Clear cart and coupon
        cart_items.delete()
        request.session.pop("coupon_code", None)

        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect("order_history")

        # GET request - show checkout page
    customer = get_object_or_404(Customer, user=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart).select_related(
        "book__details"
    )
    subtotal = sum(item.book.price * item.quantity for item in cart_items)
    discount = Decimal("0.00")
    coupon = None
    coupon_code = request.session.get("coupon_code")
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            discount = (
                subtotal * Decimal(coupon.discount_percent) / Decimal("100")
            )
        except Coupon.DoesNotExist:
            pass
    tax = subtotal * TAX_RATE
    total = subtotal + tax - discount
    return render(
        request,
        "orders/checkout.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "tax": tax,
            "discount": discount,
            "total": total,
            "coupon": coupon,
        },
    )


@login_required
def view_order_history(request):
    try:
        customer = Customer.objects.get(user=request.user)
        orders = customer.order_set.all().order_by("-created_at")
    except Customer.DoesNotExist:
        orders = []
    return render(request, "orders/order_history.html", {"orders": orders})
