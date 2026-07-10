from django.urls import path
from .views import tenant_list, add_tenant, tenant_detail, delete_tenant, hard_delete_tenant, tenant_profile_details

urlpatterns = [
    path('', tenant_list, name='tenant_list'),
    path('add/', add_tenant, name='add_tenant'),
    path('<int:tenant_id>/', tenant_detail, name='tenant_detail'),
    path('<int:tenant_id>/delete/', delete_tenant, name='delete_tenant'),
    path('<int:tenant_id>/hard-delete/',
         hard_delete_tenant, name='hard_delete_tenant'),
    path('<int:tenant_id>/profile-details/',
         tenant_profile_details, name='tenant_profile_details'),
]
