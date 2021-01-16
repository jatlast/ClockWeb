# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponseRedirect
# from django.urls import reverse, reverse_lazy
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template import Context
from .models import Address
from repairer.models import Repairer
#from django.contrib.auth import get_user_model

import traceback


address_fields_viewable_by_everyone = [
        # 'id',
        # 'user_fk',
        # 'date_created',
        'nickname',
        # 'address_type',
        'contact_name',
        'contact_phone',
        'address',
        'address_other',
        'locality_disctrict',
        'place_city',
        'district_prefectures',
        'region_state',
        'postcode',
        'country',
        'latitude',
        'longitude',
#        'location',
        'relevance',
        'accuracy',
    ]

#########################
# For Debugging forms #
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
#########################
class AddressCreateView(CreateView):
    model = Address
    fields = address_fields_viewable_by_everyone
    context_object_name = 'address'
    template_name = 'address/add.html'

    def form_valid(self, form):
        longitude = form.cleaned_data['longitude']
        latitude = form.cleaned_data['latitude']
        form.instance.user_fk = self.request.user
        form.instance.location = Point(longitude, latitude, srid=4326)
        response = super().form_valid(form)
        return response

class AddressDetailView(DetailView):
    model = Address
    context_object_name = 'address'
    template_name = 'address/address.html'

class AddressUpdateView(UpdateView):
    model = Address
    fields = address_fields_viewable_by_everyone
    context_object_name = 'address_update'
    template_name = 'address/update.html'

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     response.set_cookie('user_type', 'address', 3600 * 24 * 365 * 2) # = 63,072,000 seconds = 2 years
    #     return response

class AddressListView(ListView):
#    model = Address
    context_object_name = 'addresses'
    template_name = 'address/addresses.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        try:
            return Address.objects.filter(user_fk_id__exact=self.request.user)
        except:
            return None

class AddressDeleteView(DeleteView):
    model = Address
    success_url = '/address/'

class RepairersNearbyView(DetailView):
    model = Address
    context_object_name = 'address'
    template_name = 'address/nearby.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        context = super(RepairersNearbyView, self).get_context_data(**kwargs)
        context['debug'] = Context({"foo": "bar"})
        context['debug']['nickname'] = context['address'].location

        try:
            context['address_list'] = Address.objects.exclude(user_fk_id=context['address'].user_fk_id).annotate(distance=Distance('location', context['address'].location)).order_by('distance')[0:5]

            context['repairer_list'] =  Context({"foo": "bar"})

            repairer_count = 1
            for address in context['address_list']:
                repairer = Repairer.objects.get(user_fk_id=address.user_fk_id)
                context['repairer_list']['repairer_count'] = repairer_count
                context['repairer_list']['id'] = repairer.id
                context['repairer_list']['distance'] = address.distance
                context['repairer_list']['address'] = address.address
                context['repairer_list']['address_other'] = address.address_other
                context['repairer_list']['place_city'] = address.place_city
                context['repairer_list']['region_state'] = address.region_state
                context['repairer_list']['postcode'] = address.postcode
                context['repairer_list']['contact_phone'] = address.contact_phone
                context['repairer_list']['experience_in_years'] = repairer.experience_in_years
                context['repairer_list']['first_name'] = repairer.first_name
                context['repairer_list']['last_name'] = repairer.last_name
                context['repairer_list'].push()
                repairer_count += 1
            return context
        except Exception as e:
            trace_back = traceback.format_exc()
            context['debug']['exception'] = str(e) + " " + str(trace_back)
            return context

