from django.urls import path
from .views import ClockListCustomerView, ClockDetailCustomerView, ClockDetailRepairerView, ClockCreateView, ClockUpdateCustomerView, ClockUpdateRepairerView, ClockRepairEstimateView, ClocktypesListView

urlpatterns = [
    # List
#    path('', ClockListView.as_view(), name='clocks'),
    path('customer/', ClockListCustomerView.as_view(), name='customer_clocks'),

    # List - Clocktypes
    path('clocktypes/', ClocktypesListView.as_view(), name='clocktypes'),

    # Details
#    path('<int:pk>/', ClockDetailView.as_view(), name='clock'),
    path('customer/<int:pk>/', ClockDetailCustomerView.as_view(), name='customer_clock'),
    path('repairer/<int:pk>/', ClockDetailRepairerView.as_view(), name='repairer_clock'),
    # Create
    path('add/', ClockCreateView.as_view(), name='clock_add'),
    # Update
    path('customer/<int:pk>/update/', ClockUpdateCustomerView.as_view(), name='customer_clock_update'),
    path('repairer/<int:pk>/update/', ClockUpdateRepairerView.as_view(), name='repairer_clock_update'),
    # Estimate Repair Cost Dynamically
    path('<int:pk>/estimate/', ClockRepairEstimateView.as_view(), name='clock_estimate'),
]
