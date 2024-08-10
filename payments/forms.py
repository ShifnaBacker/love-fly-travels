from django import forms
from .models import Service

class PaymentForm(forms.Form):
    customer_name = forms.CharField(
        label='Customer Name', 
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )
    customer_email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email' })
    )
    customer_contact_india = forms.CharField(
        label='Mobile Number', 
        max_length=15, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your mobile number'})
    )
    customer_contact_other = forms.CharField(
        label='UAE Mobile Number', 
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter UAE mobile number (optional)'})
    )
    feedback = forms.CharField(
        label='Remarks', 
        widget=forms.Textarea(attrs={'placeholder': 'Enter your remarks (optional)'}), 
        required=False
    )
    service = forms.ModelChoiceField(
        label='Service', 
        queryset=Service.objects.all(),
        widget=forms.Select()  # Initial widget without a placeholder
    )
    custom_amount = forms.DecimalField(
        label='Amount', 
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a default option as the first element in the service choices
        self.fields['service'].choices = [("", "Select a service")] + list(self.fields['service'].choices)

