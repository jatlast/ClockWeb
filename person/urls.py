from django.urls import path
from .views import PersonListView, PersonDetailView, PersonCreateView, PersonUpdateView

urlpatterns = [
    path('', PersonListView.as_view(), name='persons'),
    path('<int:pk>/', PersonDetailView.as_view(), name='person'),
    path('<int:pk>/update/', PersonUpdateView.as_view(), name='person_update'),
    path('create/', PersonCreateView.as_view(), name='person_create'),
]
