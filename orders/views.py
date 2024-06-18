# views.py
import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re


from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct, Shipment
import json
from store.models import Product
from .forms import MpesaPaymentForm

def payments(request):
    body = json.loads(request.body)
    
    # store transaction details inside payment model
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    if payment.status == 'Completed':
        order.payment = payment
        order.is_ordered = True
        order.save()

        # move the cart items to order product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variation.set(product_variation)
            orderproduct.save()

            # reduce the quantity of sold items
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # clear cart
        CartItem.objects.filter(user=request.user).delete()

        # send order received email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    # send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)

def mpesa_payment(request):
    if request.method == 'POST':
        transID = request.POST.get('transID')
        orderID = request.POST.get('orderID')
        
        # validate transID to accept only 10 alphanumeric characters
        if not re.match(r'^[a-zA-Z0-9]{10}$', transID):
            messages.error(request, 'Payment ID must be exactly 10 alphanumeric characters.')
            return redirect('place_order')
        
        if Payment.objects.filter(payment_id=transID).exists():
            messages.error(request, 'Payment with this transaction ID already exists.')
            return redirect('place_order')  
        
        try:
            order = Order.objects.get(order_number=orderID, is_ordered=False)
            payment = Payment(
                user=request.user,
                payment_id=transID,
                payment_method='mpesa',
                amount_paid=order.order_total,
                status='Pending',
            )
            payment.save()

            order.payment = payment
            order.save()
            # move the cart items to order product table
            cart_items = CartItem.objects.filter(user=request.user)
            
            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                orderproduct.payment = payment
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                orderproduct.save()

                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.variations.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variation.set(product_variation)
                orderproduct.save()

                # reduce the quantity of sold items
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()
                
            # clear cart
            CartItem.objects.filter(user=request.user).delete()
            
            messages.success(request, 'Your payment has been received and is awaiting confirmation.')
            return redirect('order_complete')  # Or any other appropriate view

        except Order.DoesNotExist:
            messages.error(request, 'Order not found')
            return redirect('checkout')  # Or any other appropriate view

    return redirect('checkout')

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
   
    tax = 0
    grand_total = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.county = form.cleaned_data['county']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.is_shipped = form.cleaned_data['is_shipped']
            data.location = form.cleaned_data['location']
            data.save()
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            if data.is_shipped:
                shipment = Shipment(order=order, location=data.location)
                shipment.save()

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            
            return render(request, 'orders/payments.html', context)
    else:
        initial_data = {
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'phone': current_user.phone_number,
            'email': current_user.email,
            'address_line_1': current_user.address,
            'county': current_user.county,
            'city': current_user.city,
        }
        form = OrderForm(initial=initial_data)

        context = {
            'form': form,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,
        }
    return redirect('checkout')

def update_payment_status(request, payment_id):
    try:
        payment = Payment.objects.get(payment_id=payment_id)
        payment.status = 'Completed'
        payment.save()

        # Update the order status
        order = Order.objects.get(payment=payment)
        order.is_ordered = True
        order.save()

        # Move the cart items to the order product table
        cart_items = CartItem.objects.filter(user=order.user)
        for item in cart_items:
            orderproduct = OrderProduct.objects.create(
                order=order,
                payment=payment,
                user=order.user,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.price,
                ordered=True,
            )
            orderproduct.variation.set(item.variations.all())
            orderproduct.save()

            # Reduce the quantity of sold items
            item.product.stock -= item.quantity
            item.product.save()

        # Clear the cart
        cart_items.delete()

        # Send order received email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': order.user,
            'order': order,
        })
        to_email = order.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        messages.success(request, 'Your payment has been completed and your order is confirmed.')
        return redirect(f'order_complete?order_number={order.order_number}&payment_id={payment.payment_id}')

    except Payment.DoesNotExist:
        messages.error(request, 'Payment not found')
        return redirect('home')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('home')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        
        subtotal = sum(item.product_price * item.quantity for item in ordered_products)
        
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


@login_required
def notification_count(request):
    # Filter shipments for the logged-in user
    user_shipments = Shipment.objects.filter(order__user=request.user, notify=True, received=False)
    arrival_count = user_shipments.count()
    shipments = user_shipments.filter(arrived=True)

    return render(request, 'orders/notification.html', {'arrival_count': arrival_count, 'shipments': shipments})

@login_required
def mark_as_read(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    
    # Ensure the shipment belongs to the logged-in user
    if shipment.order.user == request.user:
        shipment.received = True
        shipment.save()
        messages.success(request, 'Shipment marked as received.')
    else:
        messages.error(request, 'You do not have permission to mark this shipment as received.')

    return redirect('notification_count')
