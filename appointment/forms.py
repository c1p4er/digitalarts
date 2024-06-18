from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment, Payment

from .validators import validate_payment_id, validate_phone_number

class AppointmentForm(forms.ModelForm):
    
    phone_number = forms.CharField(
        max_length=10,
        validators=[validate_phone_number],
        help_text='Enter a 10 digits phone number'
    )
    
    class Meta:
        model = Appointment
        fields = ['email', 'phone_number', 'date', 'time', 'location', 'message']
        
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }


class PaymentForm(forms.ModelForm):
    payment_id = forms.CharField(
        max_length=10,
        validators=[validate_payment_id],
        help_text='Enter a 10 characters without spaces'
    )
    
    class Meta:
        model = Payment
        fields = ['payment_id']
        
        widgets = {
            'payment_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_payment_id(self):
        payment_id = self.cleaned_data.get('payment_id')
        if Payment.objects.filter(payment_id=payment_id).exists():
            raise ValidationError('This payment ID is already used.')
        return payment_id