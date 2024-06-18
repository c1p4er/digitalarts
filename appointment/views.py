from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import uuid
from .models import Service, Appointment, Payment, Receipt
from .forms import AppointmentForm, PaymentForm

@login_required
def services(request):
    services = Service.objects.all()
    return render(request, 'appointment/services.html', {'services': services})

@login_required
def book_appointment(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.service = service
            appointment.status = 'pending'
            appointment.save()
            # Redirect to payment page
            return redirect('make_payment', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'appointment/book_appointment.html', {'form': form, 'service': service})

@login_required
def make_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.appointment = appointment
            payment.amount = appointment.service.price
            payment.status = 'pending'
            payment.save()
            return redirect('appointment_detail', appointment_id=appointment.id)
    else:
        form = PaymentForm()
    return render(request, 'appointment/make_payment.html', {'form': form, 'appointment': appointment})

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    payment = Payment.objects.filter(appointment=appointment).first()
    return render(request, 'appointment/appointment_detail.html', {'appointment': appointment, 'payment': payment})

@login_required
def confirm_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        if request.POST.get('action') == 'confirm':
            payment.status = 'confirmed'
            payment.appointment.status = 'booked'
            payment.save()
            payment.appointment.save()

            # Check if a receipt already exists to prevent duplicates
            if not Receipt.objects.filter(payment=payment).exists():
                # Generate a unique receipt number
                receipt_number = str(uuid.uuid4()).replace('-', '').upper()[:20]
                Receipt.objects.create(
                    appointment=payment.appointment,
                    payment=payment,
                    receipt_number=receipt_number
                )

    return redirect('dashboard')

@login_required
def receipt_detail(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    # Check if the logged-in user is the owner of the appointment
    if receipt.appointment.user != request.user:
        return HttpResponseForbidden("You are not allowed to view this receipt.")
    return render(request, 'appointment/receipt.html', {'receipt': receipt})

@login_required
def receipts(request):
    receipts = Receipt.objects.filter(appointment__user=request.user)
    context = {
        'receipts': receipts
    }
    return render(request, 'appointment/receipts.html', context)

@login_required
def pending_appointments_list(request):
    pending_appointments = Appointment.objects.filter(user=request.user, status='pending')
    return render(request, 'appointment/pending_appointments.html', {'pending_appointments': pending_appointments})

@login_required
def booked_appointments_list(request):
    booked_appointments = Appointment.objects.filter(user=request.user, status='booked', payment__status='confirmed')
    return render(request, 'appointment/booked_appointments.html', {'booked_appointments': booked_appointments})