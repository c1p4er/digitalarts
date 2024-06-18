from django.db import models
from accounts.models import Supplier
from django.utils import timezone

from .validators import validate_payment_id

class TenderRequest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']



class TenderResponse(models.Model):
    tender_request = models.ForeignKey(TenderRequest, on_delete=models.CASCADE, related_name='responses')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    admin_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    payable = models.BooleanField(default=False) 

    def __str__(self):
        return f"Response to {self.tender_request.title} by {self.supplier.username}"

    class Meta:
        ordering = ['created_at']
        
    """once the payable field is set to True, the payment is created"""
    def save(self, *args, **kwargs):
        if self.payable:
            Payment.objects.create(tender_response=self, amount=self.tender_request.budget)
        super().save(*args, **kwargs)

class Payment(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    )
    
    tender_response = models.ForeignKey(TenderResponse, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_id = models.CharField(max_length=10, unique=True, help_text='Enter a 10 characters without spaces', validators=[validate_payment_id])  
    status = models.CharField(max_length=10, default='pending', choices=STATUS)  # New field
    paid = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"Payment for {self.tender_response.tender_request.title}"

    class Meta:
        ordering = ['created_at']
