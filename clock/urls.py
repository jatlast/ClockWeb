from django.urls import path
from .views import ClockListView, ClockDetailView, ClockCreateView, ClockUpdateView, ClockRepairEstimateView, ClocktypesListView

# , ClockListCustomerView
# , ClockDetailCustomerView, ClockDetailRepairerView
# , ClockUpdateCustomerView, ClockUpdateRepairerView
urlpatterns = [
    # List
    path('', ClockListView.as_view(), name='clocks'),
#    path('customer/', ClockListCustomerView.as_view(), name='customer_clocks'),

    # List - Clocktypes
    path('clocktypes/', ClocktypesListView.as_view(), name='clocktypes'),
    # path('clocktypes/<uuid:pk>', ClocktypesListView.as_view(), name='clocktypes'),

    # Details
    path('<int:pk>/', ClockDetailView.as_view(), name='clock'),
    # path('customer/<int:pk>/', ClockDetailCustomerView.as_view(), name='customer_clock'),
    # path('repairer/<int:pk>/', ClockDetailRepairerView.as_view(), name='repairer_clock'),
    # Create
    path('add/', ClockCreateView.as_view(), name='clock_add'),
    # Update
    path('<int:pk>/update/', ClockUpdateView.as_view(), name='clock_update'),
    # path('customer/<int:pk>/update/', ClockUpdateCustomerView.as_view(), name='customer_clock_update'),
    # path('repairer/<int:pk>/update/', ClockUpdateRepairerView.as_view(), name='repairer_clock_update'),
    # Estimate Repair Cost Dynamically
    path('<int:pk>/estimate/', ClockRepairEstimateView.as_view(), name='clock_estimate'),
#    path('/estimate/', ClockRepairEstimateView.as_view(), name='clock_estimate'),
]
