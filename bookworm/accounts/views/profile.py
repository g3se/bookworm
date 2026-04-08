from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..forms import ChangePasswordForm, EditProfileForm


# FIXME profile HTMLs and URLs are missing
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
            return redirect("profile")
        else:
            messages.error(
                request,
                "Failed to update profile. Please correct the errors below.",
            )
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def change_password_view(request):
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
            update_session_auth_hash(
                request, request.user
            )  # Keep the user logged in after password change
            messages.success(request, "Password changed successfully.")
            return redirect("profile")
    else:
        form = ChangePasswordForm()

    return render(request, "accounts/change_password.html", {"form": form})


# TODO implement; maybe move; maybe also add `@login_required` or other
# decorator if needed.
def edit_address_view(request):
    raise NotImplementedError()
