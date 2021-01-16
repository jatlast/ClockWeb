from django.urls import path
from .views import AddressCreateView, AddressListView, AddressDetailView, AddressUpdateView, AddressDeleteView, RepairersNearbyView

urlpatterns = [
    # List
    path('', AddressListView.as_view(), name='addresses'),
    # Details
    path('<int:pk>/', AddressDetailView.as_view(), name='address'),
    # Create
    path('add/', AddressCreateView.as_view(), name='address_add'),
    # Update
    path('<int:pk>/update/', AddressUpdateView.as_view(), name='address_update'),
    # Delete
    path('<int:pk>/delete/', AddressDeleteView.as_view(), name='address_delete'),
    # Repairers Near This Address
    path('<int:pk>/nearby/', RepairersNearbyView.as_view(), name='repairers_nearby'),

]
