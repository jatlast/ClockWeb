from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
# from django.contrib.gis.geos import Point
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Repairer
from address.models import Address
from django.template import Context
import traceback
# Decorators to force users to be logged in to access the different Views.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

repairer_fields_viewable_by_everyone = [
        'first_name',
        'last_name',
        'company_name',
        'phone',
        'email',
        'hide_my_address',
        'hide_my_phone',
        'hide_my_email',
        'hide_my_hourly_rate',
        'hourly_rate',
        'experience_in_years',
        'still_accepting_jobs',
        'makes_service_calls',
        'service_call_hours_minimum',
        'repairs_grandfathers',
        'repairs_tubular_grandfathers',
        'packs_grandfathers_for_shipping',
        'moves_grandfathers',
        'repairs_cuckoos',
        'repairs_atmospherics',
        'repairs_anniversarys',
        'repairs_most_mechanical',
        'repairs_most_quartz',
        'road_time_minutes_included',
        'road_time_minutes_maximum',
        'personal_description',
        'image_1',
        'image_2',
        'image_3',
        'image_4',
        'image_5',
    ]

@method_decorator(login_required, name='dispatch')
class RepairerListView(ListView):
    model = Repairer
    context_object_name = 'repairers'
    template_name = 'repairer/repairers.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        else:
            context = super(RepairerListView, self).get_context_data(**kwargs)
            context['repairers'] = Repairer.objects.filter(user_fk_id__exact=self.request.user)
            return context


@method_decorator(login_required, name='dispatch')
class RepairerDetailView(DetailView):
    model = Repairer
    context_object_name = 'repairer'
    template_name = 'repairer/repairer.html'

    def get_context_data(self, **kwargs):
        context = super(RepairerDetailView, self).get_context_data(**kwargs)
        context['debug'] = Context()

        context['added_context'] = Context()
        context['added_context']['user_type'] = self.request.COOKIES.get('user_type')

        try:
            # pk = self.kwargs["pk"]
            repairer__id = self.object.id
            repairer__user_fk_id = Repairer.objects.only('user_fk_id').get(id=repairer__id).user_fk_id
            context['address'] = Address.objects.get(user_fk_id__exact=repairer__user_fk_id)
            return context
        except Exception as e:
            trace_back = traceback.format_exc()
            context['debug']['exception'] = str(e) + " " + str(trace_back)
            return context


@method_decorator(login_required, name='dispatch')
class RepairerCreateView(CreateView):
    model = Repairer
    fields = repairer_fields_viewable_by_everyone
    context_object_name = 'repairer_create'
    template_name = 'repairer/create.html'

    def form_valid(self, form):
        form.instance.user_fk = self.request.user
        response = super().form_valid(form)
        response.set_cookie('user_type', 'repairer', 3600 * 24 * 365 * 2) # = 63,072,000 seconds = 2 years
#        return super().form_valid(form)
        return response

@method_decorator(login_required, name='dispatch')
class RepairerUpdateView(UpdateView):
    model = Repairer
    fields = repairer_fields_viewable_by_everyone
    context_object_name = 'repairer_update'
    template_name = 'repairer/update.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        response.set_cookie('user_type', 'repairer', 3600 * 24 * 365 * 2) # = 63,072,000 seconds = 2 years
        return response


# Old Code

# class RepairerAboutView(DetailView):
#     model = Repairer
# #    context_object_name = 'repairer_about'
#     template_name = 'repairer/about.html'

#     def get_context_data(self, **kwargs):
#         if not self.request.user.is_authenticated:
#             return None
#         context = super(RepairerAboutView, self).get_context_data(**kwargs)
#         context['debug'] = Context()

#         try:
#             # pk = self.kwargs["pk"]
#             repairer__id = self.object.id
#             repairer__user_fk_id = Repairer.objects.only('user_fk_id').get(id=repairer__id).user_fk_id
#             context['address'] = Address.objects.get(user_fk_id__exact=repairer__user_fk_id)
#             return context
#         except Exception as e:
#             trace_back = traceback.format_exc()
#             context['debug']['exception'] = str(e) + " " + str(trace_back)
#             return context

