# context_processors.py
from .models import Shipment

def notification_count(request):
    if request.user.is_authenticated:
        user_shipments = Shipment.objects.filter(order__user=request.user, notify=True, received=False)
        arrival_count = user_shipments.count()
    else:
        arrival_count = 0
    
    return {'arrival_count': arrival_count}
