from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.gis.geos import Point
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Repairer

repairer_fields_viewable_by_everyone = [
        'first_name',
        'last_name',
        'phone_number',
        'address_street',
        'address_other',
        'city',
        'state',
        'zipcode',
        'latitude',
        'longitude',
#        'location',
        'experience_in_years',
        'still_accepting_jobs',
        'hourly_rate',
        'experience_in_years',
        'still_accepting_jobs',
        'makes_service_calls',
        'service_call_hours_minimum',
        'repairs_grandfathers',
        'repairs_tubular_grandfathers',
        'repairs_cuckoos',
        'repairs_atmospherics',
        'repairs_anniversarys',
        'repairs_most_mechanical',
        'repairs_most_quartz',
        'road_time_minutes_included',
        'road_time_minutes_maximum',
        'multiple_per_part_cost',
    ]

class RepairerListView(ListView):
#    model = Repairer
#    queryset = Repairer.objects.filter(user_fk_id__exact=request.user)
#    queryset = Repairer.objects.filter(user_fk_id__exact=7)
#    queryset = Repairer.objects.filter(last_name__exact='Three')
    context_object_name = 'repairers'
    template_name = 'repairer/repairers.html'

    def get_queryset(self):
        if self.request.user:
            return Repairer.objects.filter(user_fk_id__exact=self.request.user)
        else:
            return Repairer.objects.all()

class RepairerDetailView(DetailView):
    model = Repairer
    context_object_name = 'repairer'
    template_name = 'repairer/repairer.html'

# Form Views 
class RepairerCreateView(CreateView):
    model = Repairer
    fields = repairer_fields_viewable_by_everyone
    context_object_name = 'repairer_create'
    template_name = 'repairer/create.html'

    def form_valid(self, form):
        longitude = form.cleaned_data['longitude']
        latitude = form.cleaned_data['latitude']
        form.instance.user_fk = self.request.user
        form.instance.location = Point(longitude, latitude, srid=4326)
        return super().form_valid(form)

class RepairerUpdateView(UpdateView):
    model = Repairer
    fields = repairer_fields_viewable_by_everyone
    context_object_name = 'repairer_update'
    template_name = 'repairer/update.html'
