from django import forms
from .models import Service

class PaymentForm(forms.Form):
    customer_name = forms.CharField(label='Customer Name', max_length=100)
    customer_email = forms.EmailField(label='Email')
    customer_contact_india = forms.CharField(label='Mobile Number', max_length=15)
    customer_contact_other = forms.CharField(label='UAE Mobile Number', max_length=15, required=False)
    feedback = forms.CharField(label='Remarks', widget=forms.Textarea, required=False)
    service = forms.ModelChoiceField(label='Service', queryset=Service.objects.all())
    custom_amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
