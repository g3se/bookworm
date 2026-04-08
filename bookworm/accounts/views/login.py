from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.apps import apps

from accounts.models import Customer
from accounts.forms import (
    EditProfileForm,
    ChangePasswordForm,
    UserCreationForm,
    CustomerProfileForm,
)

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect("catalog:book_list")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("catalog:book_list")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("catalog:book_list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user)
            login(request, user)
            return redirect("catalog:book_list")
        else:
            messages.error(
                request,
                "Registration failed. Please correct the errors below."
            )
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("catalog:book_list")


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("catalog:book_list")
        else:
            messages.error(
                request,
                "Failed to update profile. Please correct the errors below."
            )
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def change_password_view(request):
    if request.method == "POST":           # ← this check was missing before
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current = form.cleaned_data["current_password"]
            new = form.cleaned_data["new_password"]
            confirm = form.cleaned_data["confirm_password"]

            if not request.user.check_password(current):
                messages.error(request, "Current password is incorrect.")
            elif new != confirm:
                messages.error(request, "New passwords do not match.")
            else:
                request.user.set_password(new)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully.")
                return redirect("profile")
    else:
        form = ChangePasswordForm()

    return render(request, "accounts/change_password.html", {"form": form})


# TODO implement; maybe move; maybe also add `@login_required` or other
# decorator if needed.
def edit_address_view(request):
    raise NotImplementedError()


# TODO implement; maybe move; maybe also add `@login_required` or other
# decorator if needed.
@login_required
def order_history_view(request):
    try:
        Order = apps.get_model("orders", "Order")
    except LookupError:
        messages.warning(request, "Order model not available.")
        orders = Order.objects.none() if False else []  # empty
    else:
        try:
            orders = Order.objects.filter(customer__user=request.user).order_by(
                "-created_at"
            )
        except Exception:
            try:
                orders = Order.objects.filter(customer=request.user).order_by(
                    "-created_at"
                )
            except Exception:
                orders = Order.objects.filter(
                    customer_id=request.user.pk
                ).order_by("-created_at")
    return render(request, "accounts/order_history.html", {"orders": orders})


@login_required
def edit_address_view(request):           # ← renamed to match urls.py
    customer, _ = Customer.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
            return redirect("catalog:book_list")
    else:
        form = CustomerProfileForm(instance=customer)  # ← moved outside POST block

    return render(request, "accounts/edit_address.html", {"form": form})  # ← moved outside POST block


@login_required
def order_history_view(request):
    try:
        customer = Customer.objects.get(user=request.user)
        orders = customer.order_set.all().order_by("-created_at")  # ← fixed from customer.orders
    except Customer.DoesNotExist:
        orders = []

    return render(request, "accounts/order_history.html", {"orders": orders})