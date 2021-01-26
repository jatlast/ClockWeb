from django.urls import path
from .views import HomePageView, AboutPageView, PageWalkthroughCustomerView, PageWalkthroughRepairerView

urlpatterns = [
    path('', HomePageView.as_view(), name='home')
    , path('about/', AboutPageView.as_view(), name='about')
    , path('cwt/', PageWalkthroughCustomerView.as_view(), name='customer_walkthrough')
    , path('rwt/', PageWalkthroughRepairerView.as_view(), name='repairer_walkthrough')
]