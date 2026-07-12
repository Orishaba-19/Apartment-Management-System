from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from dateutil.relativedelta import relativedelta

from .forms import PaymentForm
from .models import Payment, TransactionHistory


@login_required(login_url='login')
def payment_list(request):

    payments = Payment.objects.all().order_by('-payment_date')

    context = {
        'payments': payments
    }

    return render(request, 'payments/payment_list.html', context)


@login_required(login_url='login')
def delete_payment(request, payment_id):

    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == 'POST':

        # Reverse the balance calculation before deleting
        tenant = payment.tenant

        # Handle case where tenant might not have a house
        if tenant and tenant.house:
            monthly_rent = tenant.house.monthly_rent
        else:
            monthly_rent = 0

        expected_amount = monthly_rent * payment.months_paid

        # Store old values for history
        old_balance = tenant.balance

        # Reverse the balance changes
        tenant.balance -= expected_amount
        tenant.balance += payment.amount_paid

        with transaction.atomic():
            tenant.save()

            # Log the deletion (without linking to the payment we're about to delete)
            TransactionHistory.objects.create(
                tenant=tenant,
                transaction_type='payment',
                amount=-payment.amount_paid,  # Negative to indicate reversal
                previous_balance=old_balance,
                new_balance=tenant.balance,
                description=f'Payment reversal: UGX {payment.amount_paid} for {payment.months_paid} months (originally dated {payment.payment_date})',
                payment=None  # Don't link to payment since we're deleting it
            )

            # Now delete the payment
            payment.delete()

        return redirect('payment_list')

    context = {
        'payment': payment
    }

    return render(request, 'payments/delete_payment.html', context)


@login_required(login_url='login')
def add_payment(request):

    form = PaymentForm()

    if request.method == 'POST':

        form = PaymentForm(request.POST)

        if form.is_valid():

            payment = form.save(commit=False)
            tenant = payment.tenant

            # Handle security deposit and initial balance if provided
            security_deposit = form.cleaned_data.get('security_deposit')
            initial_balance = form.cleaned_data.get('initial_balance')

            old_balance = tenant.balance
            old_deposit = tenant.security_deposit

            if security_deposit is not None and security_deposit != old_deposit:
                tenant.security_deposit = security_deposit

            if initial_balance is not None and initial_balance != old_balance:
                tenant.balance = initial_balance
                old_balance = initial_balance  # Reset old_balance to reflect the initial balance set

            # Calculate expected rent for the months paid
            monthly_rent = tenant.house.monthly_rent
            expected_amount = monthly_rent * payment.months_paid

            # Update tenant balance: rent owed goes up, payment reduces it
            tenant.balance += expected_amount
            tenant.balance -= payment.amount_paid

            # Only update due date if payment covers all rent owed
            if payment.amount_paid >= expected_amount:
                tenant.next_due_date = (
                    tenant.next_due_date
                    + relativedelta(months=payment.months_paid)
                )

            with transaction.atomic():
                tenant.save()
                payment.save()

                # Log the payment transaction
                description = f'Payment: UGX {payment.amount_paid} for {payment.months_paid} month(s)'
                if payment.notes:
                    description += f' - Notes: {payment.notes}'

                TransactionHistory.objects.create(
                    tenant=tenant,
                    transaction_type='payment',
                    amount=payment.amount_paid,
                    previous_balance=old_balance,
                    new_balance=tenant.balance,
                    previous_deposit=old_deposit,
                    new_deposit=tenant.security_deposit,
                    description=description,
                    payment=payment
                )

                # Log deposit update if changed
                if security_deposit is not None and security_deposit != old_deposit:
                    TransactionHistory.objects.create(
                        tenant=tenant,
                        transaction_type='deposit_update',
                        previous_deposit=old_deposit,
                        new_deposit=security_deposit,
                        description=f'Security deposit updated from UGX {old_deposit} to UGX {security_deposit}',
                    )

            return redirect('payment_list')

    return render(request, 'payments/add_payment.html', {
        'form': form
    })
