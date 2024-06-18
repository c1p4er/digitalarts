from django.contrib import admin

from .models import Service, Appointment, Payment, Receipt

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'available')
    search_fields = ('name', 'description')
    

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'assigned_engineer', 'email', 'phone_number', 'date', 'time', 'status')
    list_filter = ('created', 'updated')
    search_fields = ('user', 'service', 'email', 'phone_number', 'assigned_engineer')
    raw_id_fields = ('user', 'service')
    autocomplete_fields = ['user', 'service', 'assigned_engineer']
    

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'payment_id', 'amount', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('appointment', 'amount', 'status')
    list_editable = ('status',)
    autocomplete_fields = ('appointment',)
    
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'payment', 'receipt_number', 'issued_at']