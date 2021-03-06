#import uuid
from django.urls import path
from .views import CustomerListView, CustomerCreateView, CustomerUpdateView, RepairersNearMeView #, CustomerDetailView
#from .forms import CreateCustomerForm
#from . import views

urlpatterns = [
    path('', CustomerListView.as_view(), name='customers'),
    # path('<uuid:pk>/', CustomerDetailView.as_view(), name='customer'),
    path('<uuid:pk>/update/', CustomerUpdateView.as_view(), name='customer_update'),
    path('create/', CustomerCreateView.as_view(), name='customer_create'),
    path('nearme/', RepairersNearMeView.as_view(), name='repairers_near_me'),
]
