from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from houses.models import House
from payments.models import Payment, TransactionHistory
from .models import Tenant


class TenantLifecycleTests(TestCase):

    def setUp(self):
        self.house = House.objects.create(
            house_number='B1',
            monthly_rent=Decimal('50000.00'),
            is_occupied=False
        )
        self.tenant = Tenant.objects.create(
            full_name='Tenant Delete Test',
            phone_number='0711111111',
            national_id='DEL001',
            move_in_date=timezone.now().date(),
            next_due_date=timezone.now().date(),
            security_deposit=Decimal('0.00'),
            balance=Decimal('0.00'),
            house=self.house
        )
        self.house.is_occupied = True
        self.house.save()

    def test_soft_delete_preserves_history_and_frees_house(self):
        response = self.client.post(
            reverse('delete_tenant', args=[self.tenant.id]),
            {}
        )

        self.assertEqual(response.status_code, 302)

        self.tenant.refresh_from_db()
        self.assertTrue(self.tenant.is_deleted)
        self.assertFalse(self.tenant.is_active)
        self.assertIsNone(self.tenant.house)

        self.house.refresh_from_db()
        self.assertFalse(self.house.is_occupied)

        self.assertTrue(
            TransactionHistory.objects.filter(
                tenant=self.tenant,
                transaction_type='tenant_deleted'
            ).exists()
        )

    def test_hard_delete_removes_tenant_and_associated_records(self):
        Payment.objects.create(
            tenant=self.tenant,
            amount_paid=Decimal('50000.00'),
            months_paid=1,
            notes='Delete flow payment'
        )
        TransactionHistory.objects.create(
            tenant=self.tenant,
            transaction_type='tenant_created',
            new_balance=Decimal('0.00'),
            new_deposit=Decimal('0.00'),
            description='Initial tenant creation'
        )

        response = self.client.post(
            reverse('hard_delete_tenant', args=[self.tenant.id]),
            {'confirm_delete': 'yes'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tenant.objects.filter(id=self.tenant.id).exists())
        self.assertFalse(Payment.objects.filter(
            tenant__id=self.tenant.id).exists())
        self.assertFalse(TransactionHistory.objects.filter(
            tenant__id=self.tenant.id).exists())

        self.house.refresh_from_db()
        self.assertFalse(self.house.is_occupied)
