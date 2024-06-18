# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, Order

@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, **kwargs):
    if instance.status == 'Completed':
        try:
            order = Order.objects.get(payment=instance)
            order.is_ordered = True
            order.save()
        except Order.DoesNotExist:
            pass


