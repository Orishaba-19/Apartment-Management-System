from django import forms
from .models import House


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['house_number', 'monthly_rent']
        widgets = {
            'house_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House number'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly rent'}),
        }
