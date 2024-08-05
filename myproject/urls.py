"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# payments/urls.py

from django.contrib import admin
from django.urls import path
from payments import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('indpay/', views.create_payment_inr, name='create_payment_inr'),
    path('uaepay/', views.create_payment_aed, name='create_payment_aed'),
    path('process_telr_payment/', views.create_payment_aed, name='process_telr_payment'),
    path('payments/success/<str:order_id>/', views.payment_success, name='payment_success'),
    path('payments/success_aed/<str:order_id>/', views.payment_success_aed, name='payment_success_aed'),
    path('payments/cancel/', views.payment_failure, name='payment_failure'),
    path('payments/razorpay_webhook/', views.razorpay_webhook, name='razorpay_webhook'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('cancellation-policy/', views.cancellation_policy, name='cancellation_policy'),
    path('contact-us/', views.contact_us, name='contact_us'),
]

