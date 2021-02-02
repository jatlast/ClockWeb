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
# The least amout of time all repairs take:
#   10 - talking to customer while taking the clock in from the customer
#   15 - dissasembly
#   15 - reasembly
#   10 - talking to customer while letting the clock out to the customer
# ------
#   40 - total
# Mechanical
#   10 - cleaning solution
#   10 - rinsing solution
#   10 - in from of the dryer
#   15 - checking pivots
#   15 - oiling back up
# ------
#   60 + 40 = 100 minutes or 1.67 hours total
# Quartz
#   10 - finding replacement movement
#   10 - finding replacement hands
# ------
#   20 + 40 = 60 minutes or 1.00 hours total
# Grandfather
#   30 - additional dissasembly
#   30 - additional reasembly
#   20 - additional cleaning solution
#   20 - additional rinsing solution
#   10 - additional in from of the dryer
#   15 - additional checking pivots
#   15 - additional oiling back up
#   30 - picking up from customer's house
#   15 - packing for delivery
#   15 - un-packing at workshop
#   30 - setting up at customer's house
# ------
#   230 + 40 + 60 = 330 minutes or 5.50 hours total
#### Double Totals ####
# Mechanical Least = 200 minutes or 3.34 hours
# Quartz Least = 120 minutes or 2.00 hours
# Grandfather Least = 200 minutes or 3.34 hours
# Thus, if quartz subtract 540 minutes or 9.00 hours


def GetClockRepairHours(repairer, clock, repair_type, distance_from_repairer):

    HOURS_MULTIPLIER = 1.00
    EXTRAS_MULTIPLIER = 0.50
    MURPHY_MULTIPLIER = 1.25
    MECHANICAL_MINIMUM = 1.67
    QUARTZ_MINIMUM = 1.00
    GRANDFATHER_MINIMUM = (3.83 + MECHANICAL_MINIMUM)
    MECHANICAL_HOURS = (MECHANICAL_MINIMUM * MURPHY_MULTIPLIER)
    QUARTZ_HOURS = (QUARTZ_MINIMUM * MURPHY_MULTIPLIER)
    GRANDFATHER_HOURS = (GRANDFATHER_MINIMUM * MURPHY_MULTIPLIER)

    clock_type_minimum_hours = {
        'Advertising' : (MECHANICAL_HOURS + 0.5),
        'Animated' : (MECHANICAL_HOURS - 0.65),
        'Anniversary' : (MECHANICAL_HOURS + 0.5),
        'Atmos' : (MECHANICAL_HOURS + 1.70),
        'Balloon' : MECHANICAL_HOURS,
        'Banjo' : MECHANICAL_HOURS,
        'Beehive' : MECHANICAL_HOURS,
        'Black Mantel' : MECHANICAL_HOURS,
        'Blinking Eye' : (MECHANICAL_HOURS - 0.75),
        'Calendar' : MECHANICAL_HOURS,
        'Carriage' : MECHANICAL_HOURS,
        'China/Porcelain' : (MECHANICAL_HOURS + 0.75),
        'Column' : MECHANICAL_HOURS,
        'Crystal Regulator' : (MECHANICAL_HOURS + 0.75),
        'Cuckoo' : (MECHANICAL_HOURS + 0.5),
        'Desk' : MECHANICAL_HOURS,
        'Dial' : MECHANICAL_HOURS,
        'Drop Trunk/Schoolhouse' : MECHANICAL_HOURS,
        'Figural' : MECHANICAL_HOURS,
        'Garnitures' : (MECHANICAL_HOURS + 0.39),
        'Gothic' : MECHANICAL_HOURS,
        'Kitchen' : MECHANICAL_HOURS,
        'Lantern' : (MECHANICAL_HOURS + 0.35),
        'Longcase/Grandfather' : GRANDFATHER_HOURS,
        'Lyre' : (MECHANICAL_HOURS + 0.75),
        'Mission' : MECHANICAL_HOURS,
        'Mantel' : MECHANICAL_HOURS,
        'Mystery' : MECHANICAL_HOURS,
        'Novelty' : MECHANICAL_HOURS,
        'Ogee' : MECHANICAL_HOURS,
        'Picture' : MECHANICAL_HOURS,
        'Portico' : (MECHANICAL_HOURS + 0.55),
        'Pillar & Scroll' : MECHANICAL_HOURS,
        'Plato' : MECHANICAL_HOURS,
        # 'Shelf' : 2.00,
        "Ship's" : (MECHANICAL_HOURS + 0.45),
        'Skeleton' : MECHANICAL_HOURS,
        'Steeple' : MECHANICAL_HOURS,
        'Swinging' : MECHANICAL_HOURS,
        'Tambour' : MECHANICAL_HOURS,
        'Tape' : MECHANICAL_HOURS,
        'Vienna Regulator' : (MECHANICAL_HOURS + 0.75),
        'Wag on the Wall' : MECHANICAL_HOURS,
        'Wall' : MECHANICAL_HOURS,
    }
    # Begin clock repair estimation logic...
    #   convert distance to road time in minutes: miles / mph * 60
    mph = 45 # assuming 45 mph because distance is "as the crow flies" so as not to use direction software
    minutes = 60 # obvious
    miles_to_minutes_multiple = minutes / mph
    one_way_minutes = (distance_from_repairer * miles_to_minutes_multiple)
    # Repairs reuire both a pick-up and a delivery, hence double round trip
    round_trip_minutes = (one_way_minutes * 2)
    # The included round trip is singular so it neecs to be doubled to reflect both the pick-up and the delivery
    repairer_round_trip_max = repairer.road_time_minutes_maximum
    # Two round trips
    repairer_round_trip_included = repairer.road_time_minutes_included
    extra_features = 0 # keep track of extra clock features

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
            est_debug_text += 'clock_type: ' + key + ' | ' + str(value) + '\n'
            break

    # All posible repair_type options ...
    if repair_type == 'House Call':
        est_hours = repairer.service_call_hours_minimum
        repairer_available = repairer.makes_service_calls
        EXTRAS_MULTIPLIER = 0.25
        # HOURS_MULTIPLIER = 1.00
    elif repair_type == 'Regulate':
        EXTRAS_MULTIPLIER = 0.125
        HOURS_MULTIPLIER = 0.25
    elif repair_type == 'Get Working':
        EXTRAS_MULTIPLIER = 0.25
        HOURS_MULTIPLIER = 0.50
    elif repair_type == 'Replace Parts':
        EXTRAS_MULTIPLIER = 0.125
        HOURS_MULTIPLIER = 0.35
    # Same as Clean & Overhaul
    elif repair_type == 'Refurbish Quartz' or repair_type == 'Refurbish Electric' or repair_type == 'Refurbish Mechanical':
        EXTRAS_MULTIPLIER = 0.50
        HOURS_MULTIPLIER = 1.00
    elif repair_type == 'Mechanical to Quartz':
        EXTRAS_MULTIPLIER = 0.25
        HOURS_MULTIPLIER = 0.75
    elif repair_type == 'Prepair to Move':
        est_hours = repairer.service_call_hours_minimum
        repairer_available = repairer.packs_grandfathers_for_shipping
        EXTRAS_MULTIPLIER = 0.25
        HOURS_MULTIPLIER = 1.25
    elif repair_type == 'Move Grandfather':
        est_hours = repairer.service_call_hours_minimum + (repairer.service_call_hours_minimum * 0.50)
        repairer_available = repairer.moves_grandfathers
        EXTRAS_MULTIPLIER = 0.25
        # HOURS_MULTIPLIER = 1.00
    else:
        est_debug_text += 'repair_type (' + repair_type + ') unrecongnized\n'

    est_debug_text += 'For ' + repair_type + ' | hours multiplier (' + str(HOURS_MULTIPLIER) + ') | extras multiplier (' + str(EXTRAS_MULTIPLIER) + ') | hours(' + str(round(est_hours,2)) + ')\n'

    # Determine if repairer works on this clock_type...
    if repairer_available and repair_type != 'Prepair to Move' and repair_type != 'Move Grandfather':
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
        else:
            repairer_available = repairer.repairs_most_mechanical

    est_debug_text += 'Available ' + str(repairer_available) + '\n'

    # check if repairer is accepting jobs and is within the maximum drive time.
    if repairer_available and repairer.still_accepting_jobs and round_trip_minutes <= repairer_round_trip_max:
        est_debug_text += 'Accepting Jobs\n'

# has_pendulum - Yes/No | 1/0
#if repair_type == 'Service Call' or repair_type == 'Prepair to Move' or repair_type == 'Move Grandfather':

        ###############################
        # Check extra features...
        ###############################

        if str(clock_type) == 'Longcase/Grandfather':
            # Assuming only Longcase/Grandfather clocks necessitate pickup and delivery
            # Check for extra drive time...
            if repairer_round_trip_included < round_trip_minutes:
                extra_for_road_time = (round_trip_minutes - repairer_round_trip_included) / minutes
                if repair_type == 'Refurbish Mechanical':
                    extra_for_road_time * 2 # 1 for pick-up & 1 for delivery
                est_hours += extra_for_road_time
                est_debug_text += 'Extra for road time for ' + str(distance_from_repairer) + ' extra road time: ' + str(extra_for_road_time) + ' | hours(' + str(round(est_hours,2)) + ')\n'
            else:
                est_debug_text += 'No extra road time: ' + str(repairer_round_trip_included) + ' < ' + str(round_trip_minutes) + ' | hours(' + str(round(est_hours,2)) + ')\n'
        else:
            # Train count only includes single train in minimum estimate
            est_debug_text += 'Has train count ' + str(clock.train_count)
            if clock.train_count > 1:
                extra_features += (clock.train_count - 1)
                est_debug_text += ' > 1'
            else:
                est_debug_text += ' < 2'
            est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

            # Wind interval only includes one day clocks in minimum estimate
            est_debug_text += 'Has wind interval ' + str(clock.wind_interval_days)
            if clock.wind_interval_days == 8:
                extra_features += 0.50
                est_debug_text += ' == 8'
            elif clock.wind_interval_days == 15:
                extra_features += 0.75
                est_debug_text += ' == 15'
            elif clock.wind_interval_days == 30:
                extra_features += 1.00
                est_debug_text += ' == 30'
            elif clock.wind_interval_days == 400:
                extra_features += 2.00
                est_debug_text += ' == 400'
            else:
                est_debug_text += ' < 8'
            est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

            # No strike included in minimum
            est_debug_text += clock.strike_type
            if clock.strike_type == 'Hourly Note':
                extra_features += 0.125
                est_debug_text += ' == Hourly Note'
            elif clock.strike_type == 'Hourly Chord' or clock.strike_type == 'Bim-Bam':
                extra_features += 0.25
                est_debug_text += ' == Hourly Chord or Bim-Bam'
            elif clock.strike_type == 'Ships Bell':
                extra_features += 2
                est_debug_text += ' == Ships Bell'
            est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

            # Has moon dial
            est_debug_text += 'Has half hour strike: ' + str(clock.has_half_hour_strike)
            if clock.has_half_hour_strike:
                extra_features += 0.125
                est_debug_text += ' == True'
            else:
                est_debug_text += ' == False'
            est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Chime cound is not included in minimum estimate
        est_debug_text += 'Has chime count ' + str(clock.chime_count)
        if clock.chime_count == 1:
            extra_features += 0.50
            est_debug_text += ' == 1'
        elif clock.chime_count == 2:
            extra_features += 0.75
            est_debug_text += ' == 2'
        elif clock.chime_count == 3:
            extra_features += 1.00
            est_debug_text += ' == 3'
        elif clock.chime_count > 3:
            extra_features += 1.25
            est_debug_text += ' > 3'
        else:
            est_debug_text += ' < 1'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Wooden gears
        est_debug_text += clock.gear_material
        if clock.gear_material == 'Wood':
            repairer_available = repairer.repairs_most_mechanical
            extra_features += 2
            est_debug_text += ' == Wood'
        else:
            est_debug_text += ' != Wood'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Has self-adjusting beat
        est_debug_text += 'Has self adjusting beat: ' + str(clock.has_self_adjusting_beat)
        if clock.has_self_adjusting_beat:
            extra_features += -0.25
            est_debug_text += ' == True'
        else:
            est_debug_text += ' == False'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Not self-adjusting strike
        est_debug_text += 'Has self adjusting strike: ' + str(clock.has_self_adjusting_strike)
        if clock.has_self_adjusting_strike:
            est_debug_text += ' == True'
        else:
            extra_features += 0.5
            est_debug_text += ' == False'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Has second hand
        est_debug_text += 'Has second hand: ' + str(clock.has_second_hand)
        if clock.has_second_hand:
            extra_features += 0.25
            est_debug_text += ' == True'
        else:
            est_debug_text += ' == False'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Has off-at-night
        est_debug_text += 'Has off-at-night: ' + str(clock.has_off_at_night)
        if clock.has_off_at_night:
            extra_features += 0.25
            est_debug_text += ' == True'
        else:
            est_debug_text += ' == False'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Has calendar
        est_debug_text += 'Has calendar: ' + str(clock.has_calendar)
        if clock.has_calendar:
            extra_features += 0.5
            est_debug_text += ' == True'
        else:
            est_debug_text += ' == False'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Has moon dial
        est_debug_text += 'Has moon dial: ' + str(clock.has_moon_dial)
        if clock.has_moon_dial:
            extra_features += 0.25
            est_debug_text += ' == True'
        else:
            est_debug_text += ' == False'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Has alarm
        est_debug_text += 'Has alarm: ' + str(clock.has_alarm)
        if clock.has_alarm:
            extra_features += 0.50
            est_debug_text += ' == True'
        else:
            est_debug_text += ' == False'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Has music box
        est_debug_text += 'Has music box: ' + str(clock.has_music_box)
        if clock.has_music_box:
            extra_features += 1
            est_debug_text += ' == True'
        else:
            est_debug_text += ' == False'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Has activity other
        est_debug_text += 'Has activity other: ' + str(clock.has_activity_other)
        if clock.has_activity_other:
            extra_features += 0.55
            est_debug_text += ' == True'
        else:
            est_debug_text += ' == False'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Has light
        est_debug_text += 'Has light: ' + str(clock.has_light)
        if clock.has_light:
            extra_features += 0.125
            est_debug_text += ' == True'
        else:
            est_debug_text += ' == False'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Check for Cable or String...
        est_debug_text += clock.drive_type
        if clock.drive_type == 'Cable' or clock.drive_type == 'String':
            extra_features += 1.5
            est_debug_text += ' == Cable or ' + clock.drive_type + ' == String'
        else:
            est_debug_text += ' != Cable or ' + clock.drive_type + ' != String'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        # Check for Electric...
        est_debug_text += clock.drive_type
        if clock.drive_type == 'Electric':
            extra_features += 1.5
            est_debug_text += ' == Electric'
        else:
            est_debug_text += ' != Electric'
        est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

        if clock.drive_type == 'Quartz':
            est_hours += (QUARTZ_HOURS - MECHANICAL_HOURS)
            est_debug_text += clock.drive_type + ' == Quartz | extras (' + str(round(extra_features,2)) + ')\n'

            est_debug_text += str(clock.dial_diameter_centimeters)
            if clock.dial_diameter_centimeters >= 35:
                extra_features += 1
                est_debug_text += ' >= 35'
            else:
                est_debug_text += ' < 35'
            est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

            est_debug_text += str(clock.has_glass_over_face)
            est_debug_text += 'Has glass/plastic over face: ' + str(clock.has_glass_over_face)
            if clock.has_glass_over_face:
                extra_features += 1
                est_debug_text += ' == True'
            else:
                est_debug_text += ' == False'
            est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'

            # Battery count only includes a single battery in minimum estimate
            est_debug_text += 'Battery count ' + str(clock.battery_count)
            if clock.battery_count > 3:
                extra_features += 1.00
                est_debug_text += ' > 3'
            elif clock.battery_count > 2:
                extra_features += 0.75
                est_debug_text += ' > 2'
            elif clock.battery_count > 1:
                extra_features += 0.50
                est_debug_text += ' > 1'
            else:
                est_debug_text += ' <= 1'
            est_debug_text += ' | extras (' + str(round(extra_features,2)) + ')\n'
        else:
            est_debug_text += clock.drive_type + ' != Quartz | extras (' + str(round(extra_features,2)) + ')\n'

        # Check if Tubular...
        if clock.has_tubes:
            repairer_available = repairer.repairs_tubular_grandfathers
            extra_features += 5.75
            est_debug_text += 'Has tubes: ' + str(clock.has_tubes) + ' == True | extras (' + str(round(extra_features,2)) + ')\n'
            # Five tubes included in the price
            if clock.tube_count >= 5:
                extra_features += 0.50
            else:
                est_debug_text += 'tube_count: ' + str(clock.tube_count) + ' < 5\n'
        else:
            est_debug_text += 'Has tubes: ' + str(clock.has_tubes) + ' != True | extras (' + str(round(extra_features,2)) + ')\n'

        est_debug_text += 'Hours ' + str(est_hours) + ' * ' + str(HOURS_MULTIPLIER) + ')\n'
        est_hours = (est_hours * HOURS_MULTIPLIER)
        est_debug_text += 'Hours ' + str(est_hours) + ' (extras ' + str(extra_features) + ' * ' + str(EXTRAS_MULTIPLIER) + ')\n'
        est_hours += (extra_features * EXTRAS_MULTIPLIER)
        est_debug_text += ' = ' + str(round(est_hours,2)) + ' Total Hours)\n'

    else:
        repairer_available = False
        est_debug_text += 'Accepting Jobs (' + str(repairer.still_accepting_jobs) + ') and ' + str(round_trip_minutes) + ' <= ' + str(repairer.road_time_minutes_maximum) + ' | hours(' + str(round(est_hours,2)) + ')\n'

    return repairer_available, one_way_minutes, est_hours, est_debug_text

@method_decorator(login_required, name='dispatch')
class ClockListView(ListView):
    # model = Clock
    context_object_name = 'clocks'
    template_name = 'clocks/clocks.html'

    def get_queryset(self):
        customer__id = Customer.objects.only('id').get(user_fk_id=self.request.user).id
        return Clock.objects.filter(customer_fk_id__exact=customer__id)

#@method_decorator(login_required, name='dispatch')
class ClocktypesListView(ListView):
    model = Clock
    context_object_name = 'clocktypes'
    template_name = 'clocks/clocktypes.html'

    def get_context_data(self, **kwargs):
        context = super(ClocktypesListView, self).get_context_data(**kwargs)
        context['debug'] = Context({"foo": "bar"})
        context['display_options'] = Context({"foo": "bar"})
        context['clocktypes_list'] = Context({"foo": "bar"})
        context['clocktypes_list'] = Clocktypes.objects.all().order_by('clock_type', 'wind_interval_days', 'train_count', 'chime_count', 'tube_count', 'battery_count')

        context['estimate_list'] =  Context({"foo": "bar"})

        user_type_cookie = self.request.COOKIES.get('user_type')

        repairer_id = 0
        if self.request.user.is_authenticated:
            context['display_options']['user_type'] = user_type_cookie
            if user_type_cookie == 'repairer':
                repairer = Repairer.objects.get(user_fk_id=self.request.user)
        else:
            context['display_options']['user_type'] = 'guest'
            repairer_id = self.request.GET.get('repairer_id', 0)
            repairer = Repairer.objects.get(id__exact=repairer_id)

        context['display_options']['repairer_first_name'] = repairer.first_name
        context['display_options']['repairer_last_name'] = repairer.last_name

        if user_type_cookie == 'repairer' or repairer_id:
            for clocktype in context['clocktypes_list']:
                distance_from_repairer = 10
                repair_type = 'Refurbish Mechanical'
                repairer_available, one_way_minutes, est_hours, est_debug_text = GetClockRepairHours(repairer, clocktype, repair_type, distance_from_repairer)
                context['estimate_list']['repair_type'] = repair_type
                context['estimate_list']['repairer_id'] = repairer.id
                context['estimate_list']['clock_pk'] = clocktype.id
                context['estimate_list']['available'] = repairer_available
                context['estimate_list']['distance_from_repairer'] = distance_from_repairer
                context['estimate_list']['one_way_minutes'] = one_way_minutes
                hourly_rate_amount = repairer.hourly_rate.amount
                context['estimate_list']['repairer_hourly_rate'] = hourly_rate_amount
                context['estimate_list']['repairer_hourly_rate_currency'] = repairer.hourly_rate.currency
                context['estimate_list']['dynamic_estimate_hours'] = est_hours
                context['estimate_list']['dynamic_estimate'] = math.ceil(est_hours * float(hourly_rate_amount))
                context['estimate_list']['debug'] = est_debug_text
                context['estimate_list'].push()
        else:
            context['debug']['text'] = 'user_type = (' + user_type_cookie + ') | repairer_id = (' + str(repairer_id) + ')\n'

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

        context['address_clock'] = Address.objects.get(id=context['form_fields']['address_clock_fk'])

        move_distance = 0.00
        if context['form_fields']['repair_type'] == 'Move Grandfather':
            context['form_fields']['address_deliver_fk'] = self.request.GET.get('address_deliver_fk', 0)
            if context['form_fields']['address_deliver_fk']:
                context['address_deliver'] = Address.objects.get(id=context['form_fields']['address_deliver_fk'])
                context['deliver_list'] = Address.objects.filter(id__exact=context['address_deliver'].id).annotate(distance=(Distance('location', context['address_clock'].location) * 1.417))
                move_distance = context['deliver_list'][0].distance.mi

        user_type_cookie = self.request.COOKIES.get('user_type')
        if user_type_cookie == 'customer':
            context['customer'] = Customer.objects.get(user_fk_id__exact=self.request.user)
        else:
            context['customer'] = Customer.objects.get(id__exact=self.request.GET.get('customer_fk', 'Empty'))

        # context['repairer_list'] = Repairer.objects.annotate(distance=Distance('location', context['customer_list'][0].location)).order_by('distance')[0:5]

        # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3835347/
        #  Table 2 - "Note: Predicted Travel Distance = Straight-Line Distance * 1.417."
        context['address_list'] = Address.objects.exclude(user_type_int__exact=0).annotate(distance=(Distance('location', context['address_clock'].location) * 1.417)).order_by('distance')[0:5]
        context['repairer_list'] = Context({"foo": "bar"})
        context['estimate_list'] = Context({"foo": "bar"})

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
            context['repairer_list']['phone'] = repairer.phone
            context['repairer_list']['email'] = repairer.email
            context['repairer_list']['hide_my_address'] = repairer.hide_my_address
            context['repairer_list']['hide_my_phone'] = repairer.hide_my_phone
            context['repairer_list']['hide_my_email'] = repairer.hide_my_email

            repair_type = context['form_fields']['repair_type']
            distance_from_repairer = (address.distance.mi + (move_distance * 1.50))

            repairer_available, one_way_minutes, est_hours, est_debug_text = GetClockRepairHours(repairer, self.object, repair_type, distance_from_repairer)

            context['repairer_list']['one_way_minutes'] = one_way_minutes
            context['repairer_list'].push()
            repairer_count += 1

            context['estimate_list']['repairer_id'] = repairer.id
            context['estimate_list']['clock_pk'] = self.object.pk

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

