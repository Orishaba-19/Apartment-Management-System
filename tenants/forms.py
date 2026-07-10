from django import forms
from .models import Tenant
from houses.models import House


class TenantForm(forms.ModelForm):

    class Meta:
        model = Tenant

        fields = [
            'full_name',
            'phone_number',
            'national_id',
            'move_in_date',
            'next_due_date',
            'house',
        ]

        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['house'].queryset = House.objects.filter(
            is_occupied=False
        )
