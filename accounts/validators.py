from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_phone_number(value):
    if not re.match(r'^\d{10}$', value):
        raise ValidationError(
            _('Phone number must be exactly 10 digits.'),
            params={'value': value},
        )