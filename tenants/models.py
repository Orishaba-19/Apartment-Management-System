from django.db import models
from houses.models import House

# Create your models here.


class Tenant(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    national_id = models.CharField(max_length=30, blank=True, null=True)

    move_in_date = models.DateField()
    next_due_date = models.DateField()

    security_deposit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    house = models.OneToOneField(
        House, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name
