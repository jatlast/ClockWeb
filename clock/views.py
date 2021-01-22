from django.views.generic import ListView, DetailView, CreateView, UpdateView #, DeleteView
from django.contrib.gis.db.models.functions import Distance
from .models import Clock, Clocktypes
from customer.models import Customer
from repairer.models import Repairer
from workorder.models import Workorder
from address.models import Address
from django.template import Context
from decimal import Decimal
from django.urls import reverse
import math
import traceback
# Decorators to force users to be logged in to access the different Views.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

clock_fields_viewable_by_everyone = [
        'nickname',
        'clock_type_fk',
        'footprint',
        'dial_diameter_centimeters',
        'has_glass_over_face',
        'train_count',
        'wind_interval_days',
        'drive_type',
        'gear_material',
        'chime_count',
        'strike_type',
        'has_half_hour_strike',
        'has_pendulum',
        'has_self_adjusting_beat',
        'has_self_adjusting_strike',
        'has_second_hand',
        'has_off_at_night',
        'has_calendar',
        'has_moon_dial',
        'has_alarm',
        'has_music_box',
        'has_activity_other',
        'has_light',
        'battery_count',
        'has_tubes',
        'tube_count',
        'choices_are_locked',
        'image_1',
        'image_2',
        'image_3',
        'image_4',
        'image_5',
    ]

clock_type_minimum_hours = {
    'Advertising' : 2.25,
    'Animated' : 2.00,
    'Anniversary' : 2.50,
    'Atmos' : 5.00,
    'Balloon' : 1.50,
    'Banjo' : 2.00,
    'Beehive' : 2.00,
    'Black Mantel' : 2.50,
    'Blinking Eye' : 1.25,
    'Calendar' : 2.25,
    'Carriage' : 1.25,
    'China/Porcelain' : 3.00,
    'Column' : 2.25,
    'Crystal Regulator' : 3.50,
    'Cuckoo' : 2.5,
    'Dial' : 1.00,
    'Drop Trunk/Schoolhouse' : 1.25,
    'Figural' : 1.00,
    'Garnitures' : 2.25,
    'Gothic' : 1.50,
    'Kitchen' : 2.25,
    'Lantern' : 2.00,
    'Longcase/Grandfather' : 7.25,
    'Lyre' : 3.50,
    'Mission' : 1.50,
    'Mantel' : 1.50,
    'Mystery' : 1.25,
    'Novelty' : 1.00,
    'Ogee' : 2.50,
    'Picture' : 2.00,
    'Portico' : 3.00,
    'Pillar & Scroll' : 2.00,
    'Plato' : 2.50,
#                    'Shelf' : 2.00,
    "Ship's" : 4.00,
    'Skeleton' : 2.00,
    'Steeple' : 2.00,
    'Swinging' : 1.50,
    'Tambour' : 2.00,
    'Tape' : 3.00,
    'Vienna Regulator' : 4.50,
    'Wag on the Wall' : 2.00,
    'Wall' : 2.00,
}

def GetClockRepairHours(repairer, clock, distance_from_repairer):
    # Begin clock repair estimation logic...
    #   convert distance to road time in minutes: miles / mph * 60
    mph = 45 # assuming 45 mph because distance is "as the crow flies" so as not to use direction software
    minutes = 60 # obvious
    miles_to_minutes_multiple = mph / minutes
    # Repairs reuire both a pick-up and a delivery, hence double round trip
    double_round_trip_minutes = (distance_from_repairer * miles_to_minutes_multiple * 4)
    # The included round trip is singular so it neecs to be doubled to reflect both the pick-up and the delivery
    double_repairer_round_trip_max = repairer.road_time_minutes_maximum * 2
    # Two round trips
    double_repairer_round_trip_included = repairer.road_time_minutes_included * 2
    extra_features = 0 # keep track of GF extra features
#            hourly = repairer.hourly_rate
    est_hours = 0.00
    repairer_available = True
    est_debug_text = '\n'

    clock_type = 'Unknown'

    try:
        clock_type = clock.clock_type_fk
    except:
        pass
    try:
        clock_type = clock.clock_type
    except:
        pass

    # Dynamically determine clock minimum hours by clock_type
    for key, value in clock_type_minimum_hours.items():
        if key == str(clock_type):
            est_hours += value
            est_debug_text += 'clock_type: ' + key + '|' + str(value) + '\n'
            break

    # check if repairer is accepting jobs and is within the maximum drive time.
    if repairer.still_accepting_jobs and double_round_trip_minutes <= double_repairer_round_trip_max:
        est_debug_text += 'Accepting Jobs\n'

# 'still_accepting_jobs',
# 'makes_service_calls',
# 'service_call_hours_minimum',
# 'repairs_grandfathers',
# 'repairs_tubular_grandfathers',
# 'repairs_cuckoos',
# 'repairs_atmospherics',
# 'repairs_anniversarys',
# 'repairs_most_mechanical',
# 'repairs_most_quartz',


        # Determine if repairer works on this clock_type...
        if str(clock_type) == 'Longcase/Grandfather':
            repairer_available = repairer.repairs_grandfathers
        elif str(clock_type) == 'Cuckoo':
            repairer_available = repairer.repairs_cuckoos
        elif str(clock_type) == 'Atmospheric':
            repairer_available = repairer.repairs_atmospherics
        elif str(clock_type) == 'Anniversary':
            repairer_available = repairer.repairs_anniversarys
        elif clock.drive_type == 'Quartz':
            repairer_available = repairer.repairs_most_quartz
            extra_features -= 2
        else:
            repairer_available = repairer.repairs_most_mechanical

        est_debug_text += 'Available ' + str(repairer_available) + '\n'

        # Exit loop if repairer is not available...
        # if repairer_available != True:
        #     break

        # Check for extra drive time...
        if double_repairer_round_trip_included < double_round_trip_minutes:
            extra_for_road_time = (double_round_trip_minutes - double_repairer_round_trip_included) / 60
            est_hours += extra_for_road_time
            est_debug_text += 'Extra for road time for ' + str(distance_from_repairer) + ' miles: ' + str(extra_for_road_time) + ' | hours(' + str(round(est_hours,2)) + ')\n'
        else:
            est_debug_text += 'No extra road time: ' + str(double_repairer_round_trip_included) + ' < ' + str(double_round_trip_minutes) + ' | hours(' + str(round(est_hours,2)) + ')\n'

        # Check for extra features...
        # Wooden gears
        if clock.gear_material == 'Wood':
            repairer_available = repairer.repairs_most_mechanical
            extra_features += 2
        else:
            est_debug_text += clock.gear_material + ' != Wood | hours(' + str(round(est_hours,2)) + ')\n'
        # Not self-adjusting strike
        if clock.has_self_adjusting_strike == False:
            extra_features += 1
        else:
            est_debug_text += 'Has self adjusting strike: ' + str(clock.has_self_adjusting_strike) + ' != False | hours(' + str(round(est_hours,2)) + ')\n'
        # Has off-at-night
        if clock.has_off_at_night:
            extra_features += 0.5
        else:
            est_debug_text += 'Has off-at-night: ' + str(clock.has_off_at_night) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
        # Has calendar
        if clock.has_calendar:
            extra_features += 0.5
        else:
            est_debug_text += 'Has calendar: ' + str(clock.has_calendar) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
        # Has moon dial
        if clock.has_moon_dial:
            extra_features += 0.25
        else:
            est_debug_text += 'Has moon dial: ' + str(clock.has_moon_dial) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
        # Has alarm
        if clock.has_alarm:
            extra_features += 1
        else:
            est_debug_text += 'Has alarm: ' + str(clock.has_alarm) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
        # Has music box
        if clock.has_music_box:
            extra_features += 1.5
        else:
            est_debug_text += 'Has music box: ' + str(clock.has_music_box) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
        # Has activity other
        if clock.has_activity_other:
            extra_features += 1
        else:
            est_debug_text += 'Has activity other: ' + str(clock.has_activity_other) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
        # Five tubes included in the price
        if clock.tube_count >= 5:
            extra_features += 0.50
        else:
            est_debug_text += 'tube_count: ' + str(clock.tube_count) + ' < 6\n'

        # Check for Cable or String...
        if clock.drive_type == 'Cable' or clock.drive_type == 'String':
            est_hours += 1.5
        else:
            est_debug_text += clock.drive_type + ' != Cable or' + clock.drive_type + ' != String | hours(' + str(round(est_hours,2)) + ')\n'
        # Check if Tubular...
        if clock.has_tubes:
            repairer_available = repairer.repairs_tubular_grandfathers
            est_hours += 5
        else:
            est_debug_text += 'Has tubes: ' + str(clock.has_tubes) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'

        est_debug_text += 'extras: ' + str(extra_features) + ' | hours(' + str(round(est_hours,2)) + ')\n'

        est_hours += (extra_features * 0.50)
    else:
        repairer_available = False
        est_debug_text += 'Accepting Jobs (' + str(repairer.still_accepting_jobs) + ') and ' + str(double_round_trip_minutes) + ' <= ' + str(repairer.road_time_minutes_maximum) + ' | hours(' + str(round(est_hours,2)) + ')\n'

    return repairer_available, est_hours, est_debug_text

@method_decorator(login_required, name='dispatch')
class ClockListView(ListView):
    # model = Clock
    context_object_name = 'clocks'
    template_name = 'clocks/clocks.html'

    def get_queryset(self):
        customer__id = Customer.objects.only('id').get(user_fk_id=self.request.user).id
        return Clock.objects.filter(customer_fk_id__exact=customer__id)

@method_decorator(login_required, name='dispatch')
class ClocktypesListView(ListView):
    model = Clock
    context_object_name = 'clocktypes'
    template_name = 'clocks/clocktypes.html'

    def get_context_data(self, **kwargs):
        context = super(ClocktypesListView, self).get_context_data(**kwargs)
        context['debug'] = Context({"foo": "bar"})
        context['clocktypes_list'] = Context({"foo": "bar"})
        context['clocktypes_list'] = Clocktypes.objects.all().order_by('clock_type')

        context['estimate_list'] =  Context({"foo": "bar"})

        user_type_cookie = self.request.COOKIES.get('user_type')
        if user_type_cookie == 'repairer':
            repairer = Repairer.objects.get(user_fk_id=self.request.user)
            for clocktype in context['clocktypes_list']:
                distance_from_repairer = 10
                repairer_available, est_hours, est_debug_text = GetClockRepairHours(repairer, clocktype, distance_from_repairer)
                context['estimate_list']['repairer_id'] = repairer.id
                context['estimate_list']['clock_pk'] = clocktype.id
                # Begin each repairer as "available" to field this estimate.

                context['estimate_list']['available'] = repairer_available
                context['estimate_list']['distance_from_repairer'] = distance_from_repairer
                hourly_rate_amount = repairer.hourly_rate.amount
                context['estimate_list']['repairer_hourly_rate'] = hourly_rate_amount
                context['estimate_list']['repairer_hourly_rate_currency'] = repairer.hourly_rate.currency
                context['estimate_list']['dynamic_estimate_hours'] = est_hours
                context['estimate_list']['dynamic_estimate'] = math.ceil(est_hours * float(hourly_rate_amount))
                context['estimate_list']['debug'] = est_debug_text
                context['estimate_list'].push()

        return context

@method_decorator(login_required, name='dispatch')
class ClockDetailView(DetailView):
    model = Clock
    context_object_name = 'clock'
    template_name = 'clocks/clock.html'

    def get_context_data(self, **kwargs):
        context = super(ClockDetailView, self).get_context_data(**kwargs)
        context['workorders'] = Workorder.objects.exclude(repair_status__exact='Paid in Full').filter(clock_fk_id__exact=self.object.pk).order_by('-date_created')

        user_type_cookie = self.request.COOKIES.get('user_type')
        if user_type_cookie == 'customer':
            context['customer_addresses'] = Address.objects.filter(user_fk_id=self.request.user)

        return context


@method_decorator(login_required, name='dispatch')
class ClockCreateView(CreateView):
    model = Clock
    fields = clock_fields_viewable_by_everyone
    context_object_name = 'clock_add'
    template_name = 'clocks/add.html'

    def form_valid(self, form):
        form.instance.user_fk = self.request.user
        customer_fk = Customer.objects.only('id').get(user_fk_id=self.request.user).id
        form.instance.customer_fk_id = customer_fk
        return super().form_valid(form)
#        return super(ClockCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("clock", args=(self.object.id,))

@method_decorator(login_required, name='dispatch')
class ClockUpdateView(UpdateView):
    model = Clock
    fields = clock_fields_viewable_by_everyone
    context_object_name = 'clock_update'
    template_name = 'clocks/update.html'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("clock", kwargs={"pk": pk})

@method_decorator(login_required, name='dispatch')
class ClockRepairEstimateView(DetailView):
    model = Clock
    context_object_name = 'clock'
    template_name = 'clocks/estimate.html'

    def get_context_data(self, **kwargs):
        context = super(ClockRepairEstimateView, self).get_context_data(**kwargs)

        context['form_fields'] = Context({"foo": "bar"})
        context['debug'] = Context({"foo": "bar"})

        context['form_fields']['repair_type'] = self.request.GET.get('repair_type', 'Empty')
        context['form_fields']['address_clock_fk'] = self.request.GET.get('address_clock_fk', 'Empty')
        context['address'] = Address.objects.get(id=context['form_fields']['address_clock_fk'])

        context['customer'] = Customer.objects.get(user_fk_id__exact=self.request.user)
        # context['repairer_list'] = Repairer.objects.annotate(distance=Distance('location', context['customer_list'][0].location)).order_by('distance')[0:5]

        context['address_list'] = Address.objects.exclude(user_type_int__exact=0).annotate(distance=Distance('location', context['address'].location)).order_by('distance')[0:5]
        context['repairer_list'] =  Context({"foo": "bar"})
        context['estimate_list'] =  Context({"foo": "bar"})

        repairer_count = 0
#        for repairer in context['repairer_list']:
        for address in context['address_list']:
            context['debug']['text'] = 'Address.address.user_fk_id = (' + str(address.user_fk_id) + ')\n'
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
            context['repairer_list']['hourly_rate'] = repairer.hourly_rate
            context['repairer_list'].push()
            repairer_count += 1

            context['estimate_list']['repairer_id'] = repairer.id
            context['estimate_list']['clock_pk'] = self.object.pk
            # Begin each repairer as "available" to field this estimate.
            context['estimate_list']['available'] = True

            # est_hours = 0.00
            # repairer_available = True
            # est_debug_text = '\n'
            distance_from_repairer = address.distance.mi

            repairer_available, est_hours, est_debug_text = GetClockRepairHours(repairer, self.object, distance_from_repairer)

            context['estimate_list']['available'] = repairer_available
            context['estimate_list']['distance_from_repairer'] = distance_from_repairer
            hourly_rate_amount = repairer.hourly_rate.amount
            context['estimate_list']['repairer_hourly_rate'] = hourly_rate_amount
            context['estimate_list']['dynamic_estimate_hours'] = est_hours
            context['estimate_list']['dynamic_estimate'] = math.ceil(est_hours * float(hourly_rate_amount))
            context['estimate_list']['debug'] = est_debug_text
            context['estimate_list'].push()
            repairer_count += 1

        return context


# Old Code

# class ClockDetailCustomerView(DetailView):
#     model = Clock
#     context_object_name = 'clock'
#     template_name = 'customer/clock.html'

#     def get_context_data(self, **kwargs):
#         if not self.request.user.is_authenticated:
#             return None
#         else:
#             context = super(ClockDetailCustomerView, self).get_context_data(**kwargs)
#             context['workorders'] = Workorder.objects.exclude(repair_status__exact='Paid in Full').filter(clock_fk_id__exact=self.object.pk).order_by('-date_created')
#             try:
#                 context['customer_list'] = Customer.objects.filter(user_fk_id__exact=self.request.user)
#                 return context
#             except:
#                 return context
 

# class ClockDetailRepairerView(DetailView):
#     model = Clock
#     context_object_name = 'clock'
#     template_name = 'repairer/clock.html'

#     def get_context_data(self, **kwargs):
#         if not self.request.user.is_authenticated:
#             return None
#         else:
#             context = super(ClockDetailRepairerView, self).get_context_data(**kwargs)
#             context['workorders'] = Workorder.objects.exclude(repair_status__exact='Paid in Full').filter(clock_fk_id__exact=self.object.pk).order_by('-date_created')
#             try:
#                 context['customer_list'] = Customer.objects.filter(user_fk_id__exact=self.request.user)
#                 return context
#             except:
#                 return context

# class ClockUpdateCustomerView(UpdateView):
#     model = Clock
#     fields = clock_fields_viewable_by_everyone
#     context_object_name = 'clock_update'
#     template_name = 'customer/clock_update.html'

#     def get_success_url(self):
#         pk = self.kwargs["pk"]
#         return reverse("customer_clock", kwargs={"pk": pk})
# # A redirect button...
# #    <input class="btn btn-secondary" type="button" value="Cancel" onclick="window.location.replace('{% url 'customer_clocks' %}')" />


# class ClockUpdateRepairerView(UpdateView):
#     model = Clock
#     fields = clock_fields_viewable_by_everyone
#     context_object_name = 'clock_update'
#     template_name = 'Repairer/clock_update.html'

#     def get_success_url(self):
#         pk = self.kwargs["pk"]
#         return reverse("repairer_clock", kwargs={"pk": pk})

