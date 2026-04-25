from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..forms import ChangePasswordForm, CustomerProfileForm, EditProfileForm
from ..models import Customer


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})


@login_required
def edit_profile_view(request):
    customer, _ = Customer.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = EditProfileForm(request.POST, instance=request.user)
        address_form = CustomerProfileForm(request.POST, instance=customer)

        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()
            messages.success(request, "Profile updated successfully.")
            # return redirect("catalog:book_list")
        else:
            messages.error(
                request,
                "Failed to update profile. Please correct the errors below.",
            )
    else:
        user_form = EditProfileForm(instance=request.user)
        address_form = CustomerProfileForm(instance=customer)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "user_form": user_form,
            "address_form": address_form,
            "customer": customer,
        },
    )


@login_required
def change_password_view(request):
    if request.method == "POST":  # ← this check was missing before
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
                # FIXME for this to work properly, a `messages` handler should
                # be present in the page template which is redirected to
                messages.success(request, "Password changed successfully.")
                return redirect("catalog:book_list")
    else:
        form = ChangePasswordForm()

    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def edit_address_view(request):  # ← renamed to match urls.py
    customer, _ = Customer.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
    else:
        form = CustomerProfileForm(
            instance=customer
        )  # ← moved outside POST block

    return render(
        request, "accounts/edit_profile.html", {"form": form}
    )  # ← moved outside POST block
