from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):

    security_deposit = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Security Deposit (UGX)'
    )

    initial_balance = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Initial Balance (UGX)'
    )

    class Meta:
        model = Payment

        fields = [
            'tenant',
            'amount_paid',
            'months_paid',
            'notes',
        ]
