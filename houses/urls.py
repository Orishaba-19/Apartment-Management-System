from django.urls import path
from .views import house_list, add_house, edit_house, delete_house

urlpatterns = [
    path('', house_list, name='house_list'),
    path('add/', add_house, name='add_house'),
    path('<int:house_id>/edit/', edit_house, name='edit_house'),
    path('<int:house_id>/delete/', delete_house, name='delete_house'),
]
