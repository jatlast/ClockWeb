from django.urls import path
from .views import ClocktypeListView, ClocktypeDetailView

urlpatterns = [
    path('', ClocktypeListView.as_view(), name='clocktypes'),
#    path('<uuid:pk>/', ClocktypeListView.as_view(), name='clocktypes'),
    path('<int:pk>/', ClocktypeDetailView.as_view(), name='clocktype'),
]
