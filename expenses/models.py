from django.db import models
from houses.models import House

# Create your models here.

class Expense(models.Model):

    EXPENSE_TYPES = (
        ('Repair', 'Repair'),
        ('Water', 'Water'),
        ('Electricity', 'Electricity'),
        ('Other', 'Other'),
    )

    house = models.ForeignKey(House, on_delete=models.CASCADE)

    expense_type = models.CharField(
        max_length=50,
        choices=EXPENSE_TYPES
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField()

    expense_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.house.house_number} - {self.expense_type}"