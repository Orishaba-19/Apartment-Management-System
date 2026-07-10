from django.db import models

# Create your models here.

class House(models.Model):
    house_number = models.CharField(max_length=10, unique=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.house_number