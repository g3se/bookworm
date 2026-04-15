from django.contrib import messages

from accounts.models import Customer
from accounts.forms import UserCreationForm
from django.contrib.auth import (
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

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
            user = form.save(commit=False)  # creates the user but doesnt save to the database yet
            user.is_staff = False  # ensures new users are not staff by default
            user.is_superuser = False  # ensures customers are not superusers
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()  # creates the user and saves to the database
            Customer.objects.create(user=user, address=form.cleaned_data.get("address", ""))
            login(request, user)
            return redirect("catalog:book_list") 
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("catalog:book_list")
