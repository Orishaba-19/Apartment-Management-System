from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import House
from .forms import HouseForm


@login_required(login_url='login')
def house_list(request):
    houses = House.objects.all().order_by('house_number')

    return render(request, 'houses/house_list.html', {
        'houses': houses
    })


@login_required(login_url='login')
def add_house(request):
    form = HouseForm()

    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('house_list')

    return render(request, 'houses/add_house.html', {
        'form': form,
        'title': 'Add House'
    })


@login_required(login_url='login')
def edit_house(request, house_id):
    house = get_object_or_404(House, id=house_id)
    form = HouseForm(instance=house)

    if request.method == 'POST':
        form = HouseForm(request.POST, instance=house)
        if form.is_valid():
            form.save()
            return redirect('house_list')

    return render(request, 'houses/edit_house.html', {
        'form': form,
        'house': house,
        'title': 'Edit House'
    })


@login_required(login_url='login')
def delete_house(request, house_id):
    house = get_object_or_404(House, id=house_id)

    if request.method == 'POST':
        house.delete()
        return redirect('house_list')

    return render(request, 'houses/delete_house.html', {
        'house': house
    })
