from django import forms
from .models import Service

class PaymentForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    customer_email = forms.EmailField()
    customer_contact_india = forms.CharField(max_length=15)
    customer_contact_other = forms.CharField(max_length=15)
    feedback = forms.CharField(widget=forms.Textarea, required=False)  # Optional field
    service = forms.ModelChoiceField(queryset=Service.objects.all())
    custom_amount = forms.DecimalField(max_digits=10, decimal_places=2)
