from django import forms
from django.contrib.messages import constants as messages

from .models import Account, UserProfile, Supplier, SupplierProfile
from .validators import validate_phone_number

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))

    phone_number = forms.CharField(
        max_length=10,
        validators=[validate_phone_number],
        help_text='Enter a 10-digit phone number without spaces or special characters.'
    )
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'county', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        # Add placeholders and classes to form inputs
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Address'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter City'
        self.fields['county'].widget.attrs['placeholder'] = 'Enter County'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match!"
            )
            
class SupplierRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))

    
    class Meta:
        model = Supplier
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'county', 'password']

    def __init__(self, *args, **kwargs):
        super(SupplierRegistrationForm, self).__init__(*args, **kwargs)
        
        # Add placeholders and classes to form inputs
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Address'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter City'
        self.fields['county'].widget.attrs['placeholder'] = 'Enter County'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
    def clean(self):
        cleaned_data = super(SupplierRegistrationForm, self).clean()
        
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match!"
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        # Add placeholders and classes to form inputs
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city',  'county', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        # Add placeholders and classes to form inputs
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Enter Address Line 1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Enter Address Line 2'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter City'
        self.fields['county'].widget.attrs['placeholder'] = 'Enter County'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
class SupplierProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = SupplierProfile
        fields = ('address_line_1', 'address_line_2', 'city',  'county', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(SupplierProfile, self).__init__(*args, **kwargs)
        
        # Add placeholders and classes to form inputs
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Enter Address Line 1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Enter Address Line 2'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter City'
        self.fields['county'].widget.attrs['placeholder'] = 'Enter County'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        