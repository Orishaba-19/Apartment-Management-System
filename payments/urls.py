from django.urls import path

from .views import payment_list, add_payment, delete_payment

urlpatterns = [

    path('', payment_list, name='payment_list'),

    path('add/', add_payment, name='add_payment'),

    path('<int:payment_id>/delete/', delete_payment, name='delete_payment'),

]
