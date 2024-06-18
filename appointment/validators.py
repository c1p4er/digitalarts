from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_payment_id(value):
    # Check if the payment ID is exactly 10 alphanumeric characters and all in uppercase
    if not re.match(r'^[A-Z0-9]{10}$', value):
        raise ValidationError(
            _('Payment ID must be exactly 10 uppercase alphanumeric characters.'),
            params={'value': value},
        )

    
def validate_phone_number(value):
    if not re.match(r'^\d{10}$', value):
        raise ValidationError(
            _('Phone number must be exactly 10 digits.'),
            params={'value': value},
        )