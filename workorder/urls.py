from django.urls import path
from .views import WorkorderCreateView, WorkorderCustomerListView, WorkorderRepairerListView, WorkorderDetailCustomerView, WorkorderDetailRepairerView, AddonsCreateRepairerView #, WorkorderUpdateView, WorkorderRepairEstimateView

urlpatterns = [
    ########## Workorders ##########
    # List
    path('customer/', WorkorderCustomerListView.as_view(), name='customer_workorders'),
    path('repairer/', WorkorderRepairerListView.as_view(), name='repairer_workorders'),
    # Details
    path('customer/<uuid:pk>/', WorkorderDetailCustomerView.as_view(), name='customer_workorder'),
    path('repairer/<uuid:pk>/', WorkorderDetailRepairerView.as_view(), name='repairer_workorder'),
    # Create
    path('add/', WorkorderCreateView.as_view(), name='workorder_add'),
    # Update
#    path('<int:pk>/update/', WorkorderUpdateView.as_view(), name='workorder_update'),

    ########## Addons ##########
    path('repairer/addons_add/', AddonsCreateRepairerView.as_view(), name='repairer_addons_add'),

]
