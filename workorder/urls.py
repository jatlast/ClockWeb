from django.urls import path
from .views import WorkorderCreateView, WorkorderListView, WorkorderDetailView, AddonsCreateView, WorkorderDeleteView

# WorkorderCreateView, WorkorderCustomerListView, WorkorderRepairerListView, WorkorderDetailCustomerView, WorkorderDetailRepairerView, AddonsCreateRepairerView, WorkorderListView #, WorkorderUpdateView, WorkorderRepairEstimateView

urlpatterns = [
    ########## Workorders ##########
    # List
    path('', WorkorderListView.as_view(), name='workorders'),
    # path('customer/', WorkorderCustomerListView.as_view(), name='customer_workorders'),
    # path('repairer/', WorkorderRepairerListView.as_view(), name='repairer_workorders'),
    # Details
    path('<uuid:pk>/', WorkorderDetailView.as_view(), name='workorder'),
    # path('customer/<uuid:pk>/', WorkorderDetailCustomerView.as_view(), name='customer_workorder'),
    # path('repairer/<uuid:pk>/', WorkorderDetailRepairerView.as_view(), name='repairer_workorder'),
    # Create
    path('add/', WorkorderCreateView.as_view(), name='workorder_add'),
#    path('estimate/', WorkorderCreateView.as_view(), name='estimate'),
    # Update
#    path('<int:pk>/update/', WorkorderUpdateView.as_view(), name='workorder_update'),
    # Delete
    path('<uuid:pk>/delete/', WorkorderDeleteView.as_view(), name='workorder_delete'),

    ########## Addons ##########
    path('addons/add/', AddonsCreateView.as_view(), name='addons_add'),

]
