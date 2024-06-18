from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Order

class OrderForm(forms.ModelForm):
    is_shipped = forms.BooleanField(required=False, label='Ship Order')
    location = forms.CharField(max_length=100, required=False, label='Location')

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'phone', 'email', 'address_line_1',
            'address_line_2', 'county', 'state', 'city', 'order_note',
            'is_shipped', 'location'
        ]


def validate_payment_id(value):
    if not re.match(r'^[a-zA-Z0-9]{10}$', value):
        raise ValidationError(
            'Payment ID must be exactly 10 alphanumeric characters.'
        )

class MpesaPaymentForm(forms.Form):
    orderID = forms.CharField(widget=forms.HiddenInput())
    transID = forms.CharField(
        max_length=10,
        validators=[validate_payment_id],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your M-Pesa Transaction ID',
            'required': True
        })
    )
