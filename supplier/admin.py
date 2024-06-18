from django.contrib import admin
from .models import TenderRequest, TenderResponse, Payment

@admin.register(TenderRequest)
class TenderRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at', 'deadline', 'is_active')
    list_filter = ('is_active', 'created_at', 'deadline')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(TenderResponse)
class TenderResponseAdmin(admin.ModelAdmin):
    list_display = ('tender_request', 'supplier', 'accepted', 'delivered', 'admin_confirmed', 'created_at', 'updated_at')
    list_filter = ('accepted', 'delivered', 'created_at')
    search_fields = ('tender_request__title', 'supplier__name')
    ordering = ('created_at',)
    autocomplete_fields = ['tender_request', 'supplier']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tender_response', 'amount', 'status', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('tender_response__tender_request__title',)
    ordering = ('created_at', 'status')
    autocomplete_fields = ['tender_response']
