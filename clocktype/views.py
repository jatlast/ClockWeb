from django.views.generic import ListView, DetailView
from .models import Clocktype

class ClocktypeListView(ListView):
    model = Clocktype
    context_object_name = 'clocktypes'
    template_name = 'clocktypes/clocktypes.html'

class ClocktypeDetailView(DetailView):
    model = Clocktype
    context_object_name = 'clocktype'
    template_name = 'clocktypes/detail.html'

