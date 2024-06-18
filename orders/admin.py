from django.contrib import admin

from .models import Payment, Order, OrderProduct, Shipment
#from .views import process_order

'''def mark_as_completed(modeladmin, request, queryset):
    queryset.update(status='Completed')
    for payment in queryset:
        order = Order.objects.get(payment=payment)
        process_order(order)
        order.is_ordered = True
        order.save()'''
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_id', 'payment_method', 'amount_paid', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__first_name', 'payment_id']
    autocomplete_fields = ['user']

    #actions = [mark_as_completed]
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0
    autocomplete_fields = ['user']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered', 'created_at']
    list_per_page = 20
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    autocomplete_fields = ['user', 'payment']
    
    inlines = [OrderProductInline]

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    
    full_name.short_description = 'Name'


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'payment', 'product',  'quantity', 'product_price', 'ordered']
    list_filter = ['ordered']
    list_per_page = 20
    search_fields = ['order__order_number', 'product__product_name']
    autocomplete_fields = ['user', 'product', 'order', 'payment']
    
@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['get_order_number', 'shipped_at', 'delivered_at', 'location', 'arrived', 'notify', 'received']
    list_filter = ['shipped_at', 'delivered_at']
    list_per_page = 20
    search_fields = ['order__order_number', 'location']
    readonly_fields = ['received']
    autocomplete_fields = ['order', 'driver']
    
    

    def get_order_number(self, obj):
        return obj.order.order_number if obj.order else None
    
    get_order_number.short_description = 'Order Number'
    get_order_number.admin_order_field = 'order__order_number'
    
    def __str__(self):
        return f'Shipment for Order: {self.order.order_number if self.order else None}'