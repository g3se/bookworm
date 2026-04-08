from django.contrib import admin

from .models import Cart, CartItem, Order, OrderItem

admin.site.register(Cart)
admin.site.register(CartItem)


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = (
        "id",
        "customer",
        "total_price",
        "is_fulfilled",
        "created_at",
    )
    list_filter = ("is_fulfilled",)
