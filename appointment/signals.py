from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .models import Payment, Receipt

@receiver(post_save, sender=Payment)
def create_receipt(sender, instance, created, **kwargs):
    if instance.status == 'confirmed':
        # Check if a receipt already exists to prevent duplicates
        if not Receipt.objects.filter(payment=instance).exists():
            # Generate a unique receipt number
            receipt_number = str(uuid.uuid4()).replace('-', '').upper()[:20]
            Receipt.objects.create(
                appointment=instance.appointment,
                payment=instance,
                receipt_number=receipt_number
            )
