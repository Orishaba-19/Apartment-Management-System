from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Tenant
from .forms import TenantForm
from payments.models import Payment, TransactionHistory
from django.utils import timezone


def tenant_list(request):

    tenants = Tenant.objects.filter(is_deleted=False)

    context = {
        'tenants': tenants,
        'today': timezone.now().date()
    }

    return render(request, 'tenants/tenant_list.html', context)


def tenant_detail(request, tenant_id):

    tenant = get_object_or_404(Tenant, id=tenant_id)
    payments = Payment.objects.filter(tenant=tenant).order_by('-payment_date')
    transaction_history = tenant.transaction_history.all()

    context = {
        'tenant': tenant,
        'payments': payments,
        'transaction_history': transaction_history,
        'today': timezone.now().date()
    }

    return render(request, 'tenants/tenant_detail.html', context)


@require_http_methods(["GET"])
def tenant_profile_details(request, tenant_id):
    """API endpoint for tenant profile popup - returns tenant details and recent transactions"""
    tenant = get_object_or_404(Tenant, id=tenant_id)
    payments = Payment.objects.filter(tenant=tenant).order_by(
        '-payment_date')[:5]  # Last 5 payments
    transaction_history = tenant.transaction_history.all()[
        :10]  # Last 10 transactions

    return render(request, 'tenants/tenant_profile_popup.html', {
        'tenant': tenant,
        'payments': payments,
        'transaction_history': transaction_history,
        'today': timezone.now().date()
    })


def add_tenant(request):

    form = TenantForm()

    if request.method == 'POST':

        form = TenantForm(request.POST)

        if form.is_valid():

            tenant = form.save()

            # mark house occupied
            house = tenant.house
            house.is_occupied = True
            house.save()

            with transaction.atomic():
                # Log tenant creation
                TransactionHistory.objects.create(
                    tenant=tenant,
                    transaction_type='tenant_created',
                    new_balance=tenant.balance,
                    new_deposit=tenant.security_deposit,
                    description=f'Tenant {tenant.full_name} created and assigned to house {house.house_number if house else "N/A"}'
                )

            return redirect('tenant_list')

    context = {
        'form': form
    }

    return render(request, 'tenants/add_tenant.html', context)


def delete_tenant(request, tenant_id):

    tenant = get_object_or_404(Tenant, id=tenant_id)

    if request.method == 'POST':

        with transaction.atomic():
            # Soft delete - mark as deleted but keep history
            tenant.is_deleted = True
            tenant.is_active = False
            tenant.deleted_at = timezone.now()

            # Free up the house
            if tenant.house:
                tenant.house.is_occupied = False
                tenant.house.save()
                tenant.house = None

            # Log tenant deletion
            TransactionHistory.objects.create(
                tenant=tenant,
                transaction_type='tenant_deleted',
                previous_balance=tenant.balance,
                previous_deposit=tenant.security_deposit,
                description=f'Tenant {tenant.full_name} soft deleted (record preserved for history)'
            )

            tenant.save()

        return redirect('tenant_list')

    context = {
        'tenant': tenant
    }

    return render(request, 'tenants/delete_tenant.html', context)


def hard_delete_tenant(request, tenant_id):
    """Permanently delete tenant and all their data - use with caution"""
    tenant = get_object_or_404(Tenant, id=tenant_id)

    if request.method == 'POST':
        # Confirmation check
        confirm_delete = request.POST.get('confirm_delete')
        if confirm_delete == 'yes':
            with transaction.atomic():
                tenant_name = tenant.full_name

                # Free up the house if assigned
                if tenant.house:
                    tenant.house.is_occupied = False
                    tenant.house.save()

                # Delete all related transactions
                TransactionHistory.objects.filter(tenant=tenant).delete()

                # Delete all payments
                Payment.objects.filter(tenant=tenant).delete()

                # Hard delete tenant
                tenant.delete()

            return redirect('tenant_list')

    context = {
        'tenant': tenant,
        'delete_type': 'hard'
    }

    return render(request, 'tenants/delete_tenant.html', context)
