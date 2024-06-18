from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import TenderRequest, TenderResponse, Payment
from accounts.models import Supplier

@login_required
def supplier_dashboard(request):
    total_tenders = TenderRequest.objects.filter(is_active=True, deadline__gt=timezone.now()).count()
    total_responses = TenderResponse.objects.filter(supplier=request.user.id).count()
    total_accepted = TenderResponse.objects.filter(supplier=request.user.id, accepted=True).count()
    total_pending = Payment.objects.filter(tender_response__supplier=request.user.id, status='pending', paid=False).count()
    total_completed = Payment.objects.filter(tender_response__supplier=request.user.id, status='completed').count()
    total_delivered = TenderResponse.objects.filter(supplier=request.user.id, delivered=True).count()
    context = {
        'total_tenders': total_tenders,
        'total_responses': total_responses,
        'total_accepted': total_accepted,
        'total_completed': total_completed,
        'total_pending': total_pending,
        'total_delivered': total_delivered
    }
    return render(request, 'supplier/dashboard.html', context)

@login_required
def tender_list(request):
    tenders = TenderRequest.objects.filter(is_active=True, deadline__gt=timezone.now()).order_by('-created_at')
    return render(request, 'supplier/tender_list.html', {'tenders': tenders})

@login_required
def tender_detail(request, tender_id):
    tender = get_object_or_404(TenderRequest, id=tender_id)
    user = request.user
    # Check if the current user has accepted this tender
    accepted = TenderResponse.objects.filter(tender_request=tender, supplier=user.supplier, accepted=True).exists()
    return render(request, 'supplier/tender_detail.html', {'tender': tender, 'accepted': accepted})

@login_required
def accept_tender(request, tender_id):
    tender = get_object_or_404(TenderRequest, id=tender_id)
    supplier = get_object_or_404(Supplier, id=request.user.id)

    if request.method == 'POST':
        TenderResponse.objects.create(
            tender_request=tender,
            supplier=supplier,
            accepted=True,
            delivered=False 
        )
        tender.is_active = False
        tender.save()
        return redirect('tender_list')

    return render(request, 'supplier/accept_tender.html', {'tender': tender})

@login_required
def view_paid_responses(request):
    paid_responses = Payment.objects.filter(status='pending')  # Filter the payments with pending status
    return render(request, 'supplier/view_paid_responses.html', {'paid_responses': paid_responses})

@login_required
def accept_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        payment.status = 'completed'
        payment.save()
        return redirect('supplier_dashboard')
    return render(request, 'supplier/accept_payment.html', {'payment': payment})

@login_required
def accepted_tenders_list(request):
    accepted_responses = TenderResponse.objects.filter(supplier=request.user.supplier, accepted=True)
    return render(request, 'supplier/accepted_tenders.html', {'accepted_responses': accepted_responses})

@login_required
def delivered_products(request):
    delivered_products = TenderResponse.objects.filter(supplier=request.user.supplier, delivered=True, admin_confirmed=True)
    return render(request, 'supplier/delivered_tenders.html', {'delivered_products': delivered_products})

@login_required
def confirmed_payments(request):
    confirmed_payments = Payment.objects.filter(tender_response__supplier=request.user.supplier, status='completed', paid=True)
    return render(request, 'supplier/confirmed_payments.html', {'confirmed_payments': confirmed_payments})


