from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_phone_number
    
class Account(AbstractUser):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True) # unique=True means that no two users can have the same username
    email = models.EmailField(unique=True) # unique=True means that no two users can have the same email address
    phone_number = models.CharField(max_length=10, validators=[validate_phone_number])
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_vendor = models.BooleanField(default=False)
    
    
    #login field
    USERNAME_FIELD = 'email' # username field
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] # required when user is created
    
   

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    #methods
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Customers'
        verbose_name_plural = 'Customers'

class Engineer(Account):
    class Meta:
        verbose_name = 'Mechanic'
        verbose_name_plural = 'Mechanic'
    
    def __str__(self):
        return str(self.email)

class Supervisor(Account):
    class Meta:
        verbose_name = 'Supervisor'
        verbose_name_plural = 'Supervisors'
    
    def __str__(self):
        return str(self.email) 

class StoreKeeper(Account):
    class Meta:
        verbose_name = 'Inventory Manager'
        verbose_name_plural = 'Inventory Manager'
    
    def __str__(self):
        return str(self.email)

class Supplier(Account):
    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
    
    def __str__(self):
        return str(self.email)
    
class Finance(Account):
    class Meta:
        verbose_name = 'Finance Officer'
        verbose_name_plural = 'Finance Officers'
    
    def __str__(self):
        return str(self.email)

class Driver(Account):
    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
    
    def __str__(self):
        return str(self.email)
    
class ShipmentManager(Account):
    class Meta:
        verbose_name = 'Shipment Manager'
        verbose_name_plural = 'Shipment Managers'
    
    def __str__(self):
        return str(self.email)
    
class UserProfile(models.Model):
    
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='userprofile/', blank=True, null=True, default='../static/images/avatars/user.png')
    city = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"
    
    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'
        
class SupplierProfile(models.Model):
    
    user = models.OneToOneField(Supplier, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='userprofile/', blank=True, null=True, default='../static/images/avatars/user.png')
    city = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"
    
    class Meta:
        verbose_name = 'Supplier Profile'
        verbose_name_plural = 'Supplier Profiles'
        

    

