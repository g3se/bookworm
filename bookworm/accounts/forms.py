from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

from .models import Customer

User = get_user_model()


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "forms-control", "placeholder": "Current Password"}
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "forms-control", "placeholder": "New Password"}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "forms-control",
                "placeholder": "Confirm New Password",
            }
        )
    )


class UserCreationForm(DjangoUserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "abc123@gmail.com"}
        ),
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "123 Main St, City, State, ZIP",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username",)


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["address"]
        widgets = {
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "123 Main St, City, State, ZIP",
                }
            )
        }
