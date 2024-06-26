# models.py
from django.db import models
from django.utils import timezone
from accounts.models import Account, Driver
from store.models import Product, Variation
from .validators import validate_payment_id

PAYMENT_CHOICES = (
    ('paypal', 'Paypal'),
    ('mpesa', 'Mpesa'),
)
STATUS = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Failed', 'Failed'),
    ('Cancelled', 'Cancelled'),
)

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=10, unique=True, validators=[validate_payment_id])
    payment_method = models.CharField(max_length=100, choices=PAYMENT_CHOICES, default='mpesa')
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    TRACKING_STATUS = (
        ('Packaging', 'Packaging'),
        ('On Transit', 'On Transit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        
    )
    
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    county = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    track = models.CharField(max_length=20, choices=TRACKING_STATUS, default='Packaging')
    tax = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)  # new field
    location = models.CharField(max_length=100, blank=True)  # new field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    def __str__(self):
        return self.first_name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.product_name

class Shipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    shipped_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True, default=timezone.now)
    location = models.CharField(max_length=100)
    arrived = models.BooleanField(default=False)
    notify = models.BooleanField(default=False)
    received = models.BooleanField(default=False) 
    
    def __str__(self):
        return f'Shipment for Order: {self.order.order_number}'
