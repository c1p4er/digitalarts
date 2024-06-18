from django.urls import path
from . import views

urlpatterns = [
    path('supplier/dashboard/', views.supplier_dashboard, name='supplier_dashboard'),
    path('supplier/tenders/', views.tender_list, name='tender_list'),
    path('supplier/tenders/<int:tender_id>/', views.tender_detail, name='tender_detail'),
    path('supplier/tenders/<int:tender_id>/accept/', views.accept_tender, name='accept_tender'),
    path('supplier/responses/', views.view_paid_responses, name='view_paid_responses'),
    path('supplier/responses/<int:payment_id>/accept/', views.accept_payment, name='accept_payment'),
    path('supplier/tenders/accepted/', views.accepted_tenders_list, name='accepted_tenders_list'),
    path('supplier/tenders/delivered/', views.delivered_products, name='delivered_products'),
    path('supplier/tenders/confirm-payment/', views.confirmed_payments, name='confirmed_payments')
]
