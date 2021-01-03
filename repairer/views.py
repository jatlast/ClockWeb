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
        'commission_percentage',
        'full_or_part_time',
        'road_time_per_minute',
        'road_time_included',
        'road_time_maximum',
        'service_call_minimum',
        'service_call_gf_chain',
        'service_call_gf_cable',
        'service_call_gf_tubular',
        'service_call_cuckoo',
        'service_call_other',
        'repair_minimum',
        'repair_gf_chain',
        'repair_gf_cable',
        'repair_gf_tubular',
        'repair_cuckoo_minimum',
        'repair_anniversary_minimum',
        'repair_atmos_minimum',
        'repair_other_minimum',
        'multiple_per_train',
        'multiple_per_activity',
        'multiple_per_wind_interval',
        'multiple_per_gf_extra',
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
