from django.urls import path

from . import views

urlpatterns = [
    path('services/', views.services, name='services'),
    path('book/<int:service_id>/', views.book_appointment, name='book_appointment'),
    path('payment/<int:appointment_id>/', views.make_payment, name='make_payment'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('confirm_payment/<int:payment_id>/', views.confirm_payment, name='confirm_payment'),
    path('appointments/pending/', views.pending_appointments_list, name='pending_appointments_list'),
    path('appointments/confirmed/', views.booked_appointments_list, name='booked_appointments_list'),
    path('receipts/', views.receipts, name='receipts'),
    path('receipt/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
    
]
