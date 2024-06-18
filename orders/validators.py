from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_payment_id(value):
    if not re.match(r'^[a-zA-Z0-9]{10}$', value):
        raise ValidationError(
            _('Payment ID must be exactly 10 alphanumeric characters.'),
            params={'value': value},
        )