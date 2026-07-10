from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from houses.models import House
from tenants.models import Tenant
from .models import Payment, TransactionHistory


class PaymentFlowTests(TestCase):

    def setUp(self):
        self.house = House.objects.create(
            house_number='A1',
            monthly_rent=Decimal('100000.00'),
            is_occupied=True
        )
        self.tenant = Tenant.objects.create(
            full_name='Test Tenant',
            phone_number='0700000000',
            national_id='TEST001',
            move_in_date=timezone.now().date(),
            next_due_date=timezone.now().date(),
            security_deposit=Decimal('0.00'),
            balance=Decimal('0.00'),
            house=self.house
        )
        self.house.is_occupied = True
        self.house.save()

    def test_add_payment_creates_payment_and_transaction_history(self):
        response = self.client.post(reverse('add_payment'), {
            'tenant': self.tenant.id,
            'amount_paid': '100000.00',
            'months_paid': '1',
            'notes': 'Rent payment',
            'security_deposit': '',
            'initial_balance': '',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.first()

        self.tenant.refresh_from_db()
        self.assertEqual(self.tenant.balance, Decimal('0.00'))

        self.assertEqual(
            TransactionHistory.objects.filter(
                payment=payment,
                transaction_type='payment'
            ).count(),
            1
        )

        history = TransactionHistory.objects.get(payment=payment)
        self.assertEqual(history.previous_balance, Decimal('0.00'))
        self.assertEqual(history.new_balance, Decimal('0.00'))

    def test_delete_payment_reverses_balance_and_logs_reversal(self):
        payment = Payment.objects.create(
            tenant=self.tenant,
            amount_paid=Decimal('50000.00'),
            months_paid=1,
            notes='Partial rent payment'
        )
        self.tenant.balance = Decimal('50000.00')
        self.tenant.save()

        response = self.client.post(
            reverse('delete_payment', args=[payment.id]),
            {'confirm': 'yes'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Payment.objects.filter(id=payment.id).exists())

        self.tenant.refresh_from_db()
        self.assertEqual(self.tenant.balance, Decimal('0.00'))

        reversal_entries = TransactionHistory.objects.filter(
            transaction_type='payment',
            amount=-payment.amount_paid
        )
        self.assertEqual(reversal_entries.count(), 1)

    def test_overdue_tenants_view_returns_days_overdue(self):
        self.tenant.next_due_date = timezone.now().date() - timedelta(days=7)
        self.tenant.save()

        response = self.client.get(reverse('overdue_tenants'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('overdue_tenants', response.context)
        overdue_data = response.context['overdue_tenants']
        self.assertEqual(len(overdue_data), 1)
        self.assertEqual(overdue_data[0]['tenant'], self.tenant)
        self.assertEqual(overdue_data[0]['days_overdue'], 7)
