from django.urls import path
from .views import ClockListView, ClockDetailView, ClockCreateView, ClockUpdateView, ClockRepairEstimateView, ClocktypesListView

urlpatterns = [
    # List
    path('', ClockListView.as_view(), name='clocks'),
    path('clocktypes/', ClocktypesListView.as_view(), name='clocktypes'),

    # Details
    path('<int:pk>/', ClockDetailView.as_view(), name='clock'),
    # Create
    path('add/', ClockCreateView.as_view(), name='clock_add'),
    # Update
    path('<int:pk>/update/', ClockUpdateView.as_view(), name='clock_update'),
    # Estimate Repair Cost Dynamically
    path('<int:pk>/estimate/', ClockRepairEstimateView.as_view(), name='clock_estimate'),
]
