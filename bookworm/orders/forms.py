from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        error_messages={"required": "Please enter your full name."},
    )
    address = forms.CharField(
        max_length=255,
        error_messages={"required": "Please enter your address."},
    )
    # Card information is unused
