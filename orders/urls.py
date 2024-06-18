from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('update_payment_status/<str:payment_id>/', views.update_payment_status, name='update_payment_status'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('mpesa_payment/', views.mpesa_payment, name='mpesa_payment'),
    path('notification/', views.notification_count, name='notification_count'),
    path('notifications/mark-as-read/<int:shipment_id>/', views.mark_as_read, name='mark_as_read'),
]
