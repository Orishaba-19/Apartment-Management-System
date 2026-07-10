from django.db import models
from tenants.models import Tenant

# Create your models here.


class Payment(models.Model):
    # Payments are for rent only. Security deposit is tracked separately on Tenant.

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    months_paid = models.PositiveIntegerField(default=1)

    notes = models.TextField(blank=True, null=True)

    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant.full_name} - {self.amount_paid}"


class TransactionHistory(models.Model):
    """Comprehensive audit trail for all transactions"""

    TRANSACTION_TYPES = [
        ('payment', 'Payment'),
        ('deposit_update', 'Security Deposit Update'),
        ('balance_adjustment', 'Balance Adjustment'),
        ('tenant_created', 'Tenant Created'),
        ('tenant_deleted', 'Tenant Deleted'),
    ]

    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name='transaction_history')
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    previous_balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    new_balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    previous_deposit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    new_deposit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    payment = models.OneToOneField(
        Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='transaction')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tenant.full_name} - {self.get_transaction_type_display()} on {self.created_at.date()}"
