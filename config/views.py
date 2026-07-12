from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from decimal import Decimal

from tenants.models import Tenant
from houses.models import House
from payments.models import Payment


@login_required(login_url='login')
def dashboard(request):

    total_tenants = Tenant.objects.filter(is_deleted=False).count()

    occupied_houses = House.objects.filter(
        is_occupied=True
    ).count()

    vacant_houses = House.objects.filter(
        is_occupied=False
    ).count()

    # Total outstanding rent owed
    total_rent_owed = sum(
        tenant.balance for tenant in Tenant.objects.filter(is_deleted=False)
    ) or Decimal('0.00')

    # Payments received this month
    today = timezone.now().date()
    month_start = today.replace(day=1)
    payments_this_month = Payment.objects.filter(
        payment_date__gte=month_start,
        payment_date__lte=today
    )
    monthly_income = sum(
        payment.amount_paid for payment in payments_this_month
    ) or Decimal('0.00')

    # Count overdue tenants
    overdue_tenants = Tenant.objects.filter(
        next_due_date__lt=today,
        is_deleted=False
    ).count()

    # Calculate rent stats by house
    house_stats = []
    houses = House.objects.all().order_by('house_number')
    for house in houses:
        tenant = Tenant.objects.filter(house=house, is_deleted=False).first()
        expected_rent = house.monthly_rent if house.is_occupied and tenant else Decimal(
            '0.00')
        actual_balance = tenant.balance if tenant else Decimal('0.00')
        status = 'Occupied' if house.is_occupied else 'Vacant'

        house_stats.append({
            'house': house,
            'tenant': tenant,
            'status': status,
            'expected_rent': expected_rent,
            'balance': actual_balance
        })

    context = {
        'total_tenants': total_tenants,
        'occupied_houses': occupied_houses,
        'vacant_houses': vacant_houses,
        'total_rent_owed': total_rent_owed,
        'monthly_income': monthly_income,
        'overdue_tenants': overdue_tenants,
        'house_stats': house_stats,
        'today': today,
    }

    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def overdue_tenants(request):

    today = timezone.now().date()
    queryset = Tenant.objects.filter(
        next_due_date__lt=today,
        is_deleted=False
    )

    overdue = []
    for tenant in queryset:
        try:
            days_overdue = (today - tenant.next_due_date).days
        except Exception:
            days_overdue = None
        overdue.append({
            'tenant': tenant,
            'days_overdue': days_overdue,
        })

    context = {
        'overdue_tenants': overdue,
        'today': today
    }

    return render(request, 'overdue_tenants.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
