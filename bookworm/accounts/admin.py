from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, User


# admin.site.register(Customer)
# admin.site.register(User)


@admin.register(User)
class CustomerUserAdmin(UserAdmin):
    def get_readonly_fields(self, request, obj=None):
        # If the user has a customer profile, lock their staff permissions
        if obj and hasattr(obj, "customer"):
            return ["is_staff", "is_superuser"]
        return []


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user", "address"]
