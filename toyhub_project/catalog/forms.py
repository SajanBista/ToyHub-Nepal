from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help texts
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = ''


class DeliveryForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="Full Name")
    phone = forms.CharField(max_length=15, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Delivery Address")


class DeliveryAddressForm(forms.Form):
    phone = forms.CharField(max_length=15, label="Phone Number")
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=255,
        label="Delivery Address"
    )
