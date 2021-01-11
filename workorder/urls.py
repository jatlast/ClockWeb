from django.urls import path
from .views import WorkorderCreateView #, WorkorderListView, WorkorderDetailView, WorkorderUpdateView, WorkorderRepairEstimateView

urlpatterns = [
    # List
#    path('', WorkorderListView.as_view(), name='workorders'),
    # Details
#    path('<int:pk>/', WorkorderDetailView.as_view(), name='workorder'),
    # Create
    path('add/', WorkorderCreateView.as_view(), name='workorder_add'),
    # Update
#    path('<int:pk>/update/', WorkorderUpdateView.as_view(), name='workorder_update'),
]
