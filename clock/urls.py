from django.urls import path
from .views import ClockListView, ClockDetailView, ClockCreateView, ClockUpdateView

urlpatterns = [
    # List
    path('', ClockListView.as_view(), name='clocks'),
    # Details
    path('<int:pk>/', ClockDetailView.as_view(), name='clock'),
    # Create
    path('add/', ClockCreateView.as_view(), name='clock_add'),
    # Update
    path('<int:pk>/update/', ClockUpdateView.as_view(), name='clock_update'),
]
