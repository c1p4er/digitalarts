from django.db import models
from accounts.models import Account, Engineer
from django.utils import timezone

class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/', blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'service'

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('booked', 'Booked'),
        ('completed', 'Completed')
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    assigned_engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='appointments', blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    date = models.DateField()
    time = models.TimeField(default=timezone.now().replace(second=0, microsecond=0))
    location = models.CharField(max_length=100)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ('-date',)
        verbose_name = 'appointment'

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed')
    )

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=10, unique=True)  # Payment ID provided by the user
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Payment for {self.appointment.service.name} by {self.appointment.user.username}"
    
class Receipt(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=20, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-issued_at',)
        verbose_name = 'receipt'

    def __str__(self):
        return f"Receipt {self.receipt_number} for {self.appointment.service.name} by {self.appointment.user.username}"
