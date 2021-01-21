#import uuid
from django.urls import path
from .views import RepairerListView, RepairerDetailView, RepairerCreateView, RepairerUpdateView
#from .forms import CreateRepairerForm
#from . import views

#, RepairerAboutView

urlpatterns = [
    path('', RepairerListView.as_view(), name='repairers'),
    path('<uuid:pk>/', RepairerDetailView.as_view(), name='repairer'),
    path('<uuid:pk>/update/', RepairerUpdateView.as_view(), name='repairer_update'),
#    path('<uuid:pk>/about/', RepairerAboutView.as_view(), name='repairer_about'),
    path('create/', RepairerCreateView.as_view(), name='repairer_create'),
]
