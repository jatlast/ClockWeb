# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponseRedirect
# from django.urls import reverse, reverse_lazy
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template import Context
from .models import Address
from repairer.models import Repairer
from customer.models import Customer
#from django.contrib.auth import get_user_model
import traceback
# Decorators to force users to be logged in to access the different Views.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

address_fields_viewable_by_everyone = [
        # 'id',
        # 'user_fk',
        # 'date_created',
        'nickname',
        # 'address_type',
        'user_type_int',
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
#@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class AddressDetailView(DetailView):
    model = Address
    context_object_name = 'address'
    template_name = 'address/address.html'

@method_decorator(login_required, name='dispatch')
class AddressUpdateView(UpdateView):
    model = Address
    fields = address_fields_viewable_by_everyone
    context_object_name = 'address_update'
    template_name = 'address/update.html'

@method_decorator(login_required, name='dispatch')
class AddressListView(ListView):
    model = Address
    context_object_name = 'addresses'
    template_name = 'address/addresses.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        else:
            context = super(AddressListView, self).get_context_data(**kwargs)
            context['debug'] = Context()
            try:
                context['customers'] = Customer.objects.filter(user_fk_id=self.request.user)
                # context['repairers'] = Repairer.objects.filter(user_fk_id=self.request.user)
                return context
            except Exception as e:
                trace_back = traceback.format_exc()
                context['debug']['exception'] = str(e) + " " + str(trace_back)
                return context

@method_decorator(login_required, name='dispatch')
class AddressDeleteView(DeleteView):
    model = Address
    success_url = '/address/'

@method_decorator(login_required, name='dispatch')
class RepairersNearbyView(DetailView):
    model = Address
    context_object_name = 'address'
    template_name = 'address/nearby.html'

    def get_context_data(self, **kwargs):
        context = super(RepairersNearbyView, self).get_context_data(**kwargs)
        context['debug'] = Context()
        context['debug']['nickname'] = context['address'].location

        try:
            # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3835347/
            #  Table 2 - "Note: Predicted Travel Distance = Straight-Line Distance * 1.417."
            context['address_list'] = Address.objects.exclude(user_type_int__exact=0).annotate(distance=(Distance('location', context['address'].location) * 1.417)).order_by('distance')[0:5]
#            context['address_list'] = Address.objects.exclude(user_type_int__exact=0).annotate(distance=Distance('location', context['address'].location)).order_by('distance')[0:5]

            context['repairer_list'] =  Context()

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
                context['repairer_list']['latitude'] = address.latitude
                context['repairer_list']['longitude'] = address.longitude
                context['repairer_list']['contact_phone'] = address.contact_phone
                context['repairer_list']['experience_in_years'] = repairer.experience_in_years
                context['repairer_list']['first_name'] = repairer.first_name
                context['repairer_list']['last_name'] = repairer.last_name
                context['repairer_list']['phone'] = repairer.phone
                context['repairer_list']['email'] = repairer.email
                context['repairer_list']['hide_my_address'] = repairer.hide_my_address
                context['repairer_list']['hide_my_phone'] = repairer.hide_my_phone
                context['repairer_list']['hide_my_email'] = repairer.hide_my_email
                context['repairer_list'].push()
                repairer_count += 1
            return context
        except Exception as e:
            trace_back = traceback.format_exc()
            context['debug']['exception'] = str(e) + " " + str(trace_back)
            return context

