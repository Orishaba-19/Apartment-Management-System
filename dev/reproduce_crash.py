from tenants.forms import TenantForm
from payments.forms import PaymentForm
from payments.models import Payment
from tenants.models import Tenant
from houses.models import House
import os
import sys
import traceback
import django
from django.test import Client
from django.utils import timezone
from decimal import Decimal

# Ensure project path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Import models and forms after Django is configured

client = Client()


def safe_request(method, path, data=None):
    try:
        if method == 'get':
            resp = client.get(path)
        else:
            resp = client.post(path, data or {})
        print(f'[{method.upper()}] {path} -> status {resp.status_code}')
        return resp
    except Exception as e:
        print(f'EXCEPTION during {method.upper()} {path}: {e}')
        traceback.print_exc()
        return None


print('Testing public endpoints...')
safe_request('get', '/')
safe_request('get', '/tenants/')
safe_request('get', '/payments/')

# Test tenant profile endpoints (create seed data if none exists)
tenant = Tenant.objects.first()
if tenant:
    print('\nFound tenant id:', tenant.id)
    safe_request('get', f'/tenants/{tenant.id}/profile-details/')
    safe_request('get', f'/tenants/{tenant.id}/')
else:
    print('\nNo tenants found in DB - creating sample data')
    # create a sample house
    house, _ = House.objects.get_or_create(house_number='A1', defaults={
        'monthly_rent': Decimal('100000.00'), 'is_occupied': False
    })
    tenant = Tenant.objects.create(
        full_name='Test Tenant',
        phone_number='0700000000',
        national_id='TST12345',
        move_in_date=timezone.now().date(),
        next_due_date=timezone.now().date(),
        security_deposit=Decimal('0.00'),
        balance=Decimal('0.00'),
        is_active=True,
        is_deleted=False,
        house=house
    )
    house.is_occupied = True
    house.save()
    print('Created tenant id:', tenant.id)
    safe_request('get', f'/tenants/{tenant.id}/profile-details/')
    safe_request('get', f'/tenants/{tenant.id}/')

# Test payment delete: create payment if none exists
payment = Payment.objects.first()
if payment:
    print('\nFound payment id:', payment.id, 'for tenant', payment.tenant_id)
    # Attempt to GET the delete page first
    safe_request('get', f'/payments/{payment.id}/delete/')
    # Attempt to POST to delete (test client bypasses CSRF)
    safe_request(
        'post', f'/payments/{payment.id}/delete/', data={'confirm': 'yes'})
else:
    print('\nNo payments found in DB - creating a sample payment')
    # create a sample payment for the tenant
    payment = Payment.objects.create(
        tenant=tenant,
        amount_paid=Decimal('100000.00'),
        months_paid=1,
        notes='Seed payment for testing'
    )
    print('Created payment id:', payment.id)
    safe_request('get', f'/payments/{payment.id}/delete/')
    safe_request(
        'post', f'/payments/{payment.id}/delete/', data={'confirm': 'yes'})


print('\n--- Additional flow tests (forms, overdue, tenant delete) ---')

# 1) Add tenant via POST form
new_house, _ = House.objects.get_or_create(house_number='B1', defaults={
                                           'monthly_rent': Decimal('120000.00'), 'is_occupied': False})
tenant_data = {
    'full_name': 'Form Tenant',
    'phone_number': '0711111111',
    'national_id': 'FORM123',
    'move_in_date': timezone.now().date().isoformat(),
    'next_due_date': (timezone.now().date()).isoformat(),
    'house': str(new_house.id),
}
resp = safe_request('post', '/tenants/add/', data=tenant_data)
if resp and resp.status_code in (302, 200):
    print('Tenant added via form. Refreshing tenant list...')
    safe_request('get', '/tenants/')
    form_tenant = Tenant.objects.filter(full_name='Form Tenant').first()
else:
    form_tenant = None

# 2) Add payment via POST form for form_tenant (or existing tenant)
target_tenant = form_tenant or tenant
if target_tenant:
    payment_form = {
        'tenant': str(target_tenant.id),
        'amount_paid': '50000.00',
        'months_paid': '1',
        'notes': 'Payment via form test',
        'security_deposit': '',
        'initial_balance': '',
    }
    safe_request('post', '/payments/add/', data=payment_form)
    # Check payments list
    safe_request('get', '/payments/')

# 3) Overdue tenants view
safe_request('get', '/overdue/')

# 4) Soft delete the form_tenant
if form_tenant:
    print('Soft deleting tenant via POST...')
    safe_request('post', f'/tenants/{form_tenant.id}/delete/')
    safe_request('get', '/tenants/')

# 5) Hard delete the tenant if exists
if form_tenant:
    print('Hard deleting tenant via POST...')
    safe_request(
        'post', f'/tenants/{form_tenant.id}/hard-delete/', data={'confirm_delete': 'yes'})
    safe_request('get', '/tenants/')

# Print last few lines of error log if exists
log_path = os.path.join(BASE_DIR, 'logs', 'error.log')
print('\nChecking logs at', log_path)
if os.path.exists(log_path):
    print('\n--- last 200 lines of log ---')
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()[-200:]
        print(''.join(lines))
else:
    print('Log file does not exist yet.')
