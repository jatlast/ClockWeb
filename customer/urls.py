#import uuid
from django.urls import path
from .views import CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView
#from .forms import CreateCustomerForm
#from . import views

urlpatterns = [
    path('', CustomerListView.as_view(), name='customers'),
    path('<uuid:pk>/', CustomerDetailView.as_view(), name='customer'),
    path('<uuid:pk>/update/', CustomerUpdateView.as_view(), name='update'),
    path('create/', CustomerCreateView.as_view(), name='create'),
]
