import requests
import json
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import PaymentForm
from .models import Service, Payment
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import razorpay

def privacy_policy(request):
    return render(request, 'payments/privacy_policy.html')


def terms_and_conditions(request):
    return render(request, 'payments/terms_and_conditions.html')

def cancellation_policy(request):
    return render(request, 'payments/cancellation_policy.html')

def contact_us(request):
    return render(request, 'payments/contact_us.html')

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_payment_inr(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            customer_email = form.cleaned_data['customer_email']
            customer_contact_india = form.cleaned_data['customer_contact_india']
            customer_contact_other = form.cleaned_data['customer_contact_other']
            feedback = form.cleaned_data['feedback']
            service = form.cleaned_data['service']
            amount = form.cleaned_data['custom_amount']

            order_amount = int(amount * 100)  # Razorpay expects the amount in paise
            currency = 'INR'
            order = razorpay_client.order.create({
                'amount': order_amount,
                'currency': currency,
                'payment_capture': '1'
            })

            payment = Payment.objects.create(
                service=service,
                amount=amount,
                currency=currency,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_contact_india=customer_contact_india,
                customer_contact_other=customer_contact_other,
                feedback=feedback,
                order_id=order['id'],
                status='pending'
            )

            return render(request, 'payments/create_payment_inr.html', {
                'form': form,
                'order_id': order['id'],
                'amount': order_amount,
                'key_id': settings.RAZORPAY_KEY_ID,
                'name': customer_name,
                'email': customer_email,
                'contact_india': customer_contact_india,
                'contact_other': customer_contact_other
            })
    else:
        form = PaymentForm()

    return render(request, 'payments/create_payment_inr.html', {'form': form})

def create_payment_aed(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            customer_email = form.cleaned_data['customer_email']
            customer_contact_india = form.cleaned_data['customer_contact_india']
            customer_contact_other = form.cleaned_data['customer_contact_other']
            feedback = form.cleaned_data['feedback']
            service = form.cleaned_data['service']
            amount = form.cleaned_data['custom_amount']

            
            currency = 'AED'

            payload = {
                'ivp_method': 'create',
                'ivp_store': settings.TELR_STORE_ID,
                'ivp_authkey': settings.TELR_AUTH_KEY,
                'ivp_cart': f'cart_{service.id}_{customer_name}',
                'ivp_test': 1,  # Change to 0 for live transactions
                'ivp_amount': amount,
                'ivp_currency': currency,
                'ivp_desc': f'Payment for {service.name}',
                'return_auth': settings.TELR_RETURN_URL,
                'return_can': settings.TELR_CANCEL_URL,
                'bill_fname': customer_name,
                'bill_email': customer_email,
                'bill_phone': customer_contact_india,
            }

            response = requests.post('https://secure.telr.com/gateway/order.json', data=payload)
            response_data = response.json()

            if response_data['order']['status']['code'] == 3:
                payment = Payment.objects.create(
                    service=service,
                    amount=amount,
                    currency=currency,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    customer_contact_india=customer_contact_india,
                    customer_contact_other=customer_contact_other,
                    feedback=feedback,
                    order_id=response_data['order']['ref'],
                    status='pending'
                )
                return redirect(response_data['order']['url'])
            else:
                return render(request, 'payments/payment_failure.html', {'error': response_data['order']['status']['text']})
    else:
        form = PaymentForm()

    return render(request, 'payments/create_payment_aed.html', {'form': form})

def payment_success(request, order_id):
    payment = Payment.objects.get(order_id=order_id)
    payment.status = 'completed'
    payment.save()

    return render(request, 'payments/payment_success.html', {'payment': payment})

def payment_success_aed(request, order_id):
    payment = Payment.objects.get(order_id=order_id)
    payment.status = 'completed'
    payment.save()

    return render(request, 'payments/payment_success.html', {'payment': payment})

def payment_failure(request):
    return render(request, 'payments/payment_failure.html')

@csrf_exempt
def razorpay_webhook(request):
    # Verify webhook signature and handle Razorpay payment updates
    webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
    request_body = request.body
    signature = request.headers.get('X-Razorpay-Signature')

    try:
        event = razorpay_client.utility.verify_webhook_signature(
            request_body, signature, webhook_secret
        )
        if event['event'] == 'payment.captured':
            order_id = event['payload']['payment']['entity']['order_id']
            payment = Payment.objects.get(order_id=order_id)
            payment.status = 'completed'
            payment.save()
            return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)
