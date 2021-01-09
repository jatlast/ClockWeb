from django.views.generic import ListView, DetailView, CreateView, UpdateView #, DeleteView
from django.contrib.gis.db.models.functions import Distance
from .models import Clock
from customer.models import Customer
from repairer.models import Repairer
from django.template import Context
from decimal import Decimal
import math

clock_fields_viewable_by_everyone = [
        'nickname',
        'clock_type_fk',
        'footprint',
        'train_count',
        'wind_interval_days',
        'drive_type',
        'gear_material',
        'chime_count',
        'strike_type',
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
        'has_tubes',
        'tube_count',
        'choices_are_locked',
        'image_1',
        'image_2',
        'image_3',
        'image_4',
        'image_5',
    ]

class ClockListView(ListView):
    # model = Clock
    context_object_name = 'clocks'
    template_name = 'clocks/clocks.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        try:
            return Clock.objects.filter(user_fk_id__exact=self.request.user)
        except:
            return None

class ClockDetailView(DetailView):
    model = Clock
    context_object_name = 'clock'
    template_name = 'clocks/clock.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        else:
            context = super(ClockDetailView, self).get_context_data(**kwargs)
            try:
                context['customer_list'] = Customer.objects.filter(user_fk_id__exact=self.request.user)
                return context
            except:
                return context
 
class ClockCreateView(CreateView):
    model = Clock
    fields = clock_fields_viewable_by_everyone
    context_object_name = 'clock_add'
    template_name = 'clocks/add.html'

    def form_valid(self, form):
        form.instance.user_fk = self.request.user
        return super().form_valid(form)

class ClockUpdateView(UpdateView):
    model = Clock
    fields = clock_fields_viewable_by_everyone
    context_object_name = 'clock_update'
    template_name = 'clocks/update.html'

class ClockRepairEstimateView(DetailView):
    model = Clock
    context_object_name = 'clock'
    template_name = 'clocks/estimate.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        else:
            context = super(ClockRepairEstimateView, self).get_context_data(**kwargs)
            try:
                context['customer_list'] = Customer.objects.filter(user_fk_id__exact=self.request.user)
                context['repairer_list'] = Repairer.objects.annotate(distance=Distance('location', context['customer_list'][0].location)).order_by('distance')[0:5]

                context['estimate_list'] =  Context({"foo": "bar"})
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
                    'Drop Trunk/School House' : 1.25,
                    'Figural' : 1.00,
                    'Garnitures' : 2.25,
                    'Gothic' : 1.50,
                    'Kitchen' : 2.25,
                    'Lantern' : 2.00,
                    'Longcase/Grandfather' : 7.25,
                    'Lyre' : 3.50,
                    'Mission' : 1.50,
                    'Mystery' : 1.25,
                    'Novelty' : 1.00,
                    'Ogee' : 2.50,
                    'Picture' : 2.00,
                    'Portico' : 3.00,
                    'Pillar & Scroll' : 2.00,
                    'Plato' : 2.50,
                    'Shelf' : 2.00,
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

                repairer_count = 0
                for repairer in context['repairer_list']:
                    context['estimate_list']['id'] = repairer.id
                    context['estimate_list']['clock_id'] = self.object.clock_type_fk
                    # Begin each repairer as "available" to field this estimate.
                    context['estimate_list']['available'] = True

                    # Begin clock repair estimation logic...
                    #   convert distance to road time in minutes: miles / mph * 60
                    mph = 45 # assuming 45 mph because distance is "as the crow flies" so as not to use direction software
                    minutes = 60 # obvious
                    miles_to_minutes_multiple = mph / minutes
                    # Repairs reuire both a pick-up and a delivery, hence double round trip
                    double_round_trip_minutes = (repairer.distance.mi * miles_to_minutes_multiple * 4)
                    # The included round trip is singular so it neecs to be doubled to reflect both the pick-up and the delivery
                    double_repairer_round_trip_max = repairer.road_time_minutes_maximum * 2
                    # Two round trips
                    double_repairer_round_trip_included = repairer.road_time_minutes_included * 2
                    extra_features = 0 # keep track of GF extra features
        #            hourly = repairer.hourly_rate
                    est_hours = 0.00
                    est_debug_text = '\n'

                    # Dynamically determine clock minimum hours by clock_type
                    for key, value in clock_type_minimum_hours.items():
                        if key == str(self.object.clock_type_fk):
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
                        if str(self.object.clock_type_fk) == 'Longcase/Grandfather':
                            context['estimate_list']['available'] = repairer.repairs_grandfathers
                        elif str(self.object.clock_type_fk) == 'Cuckoo':
                            context['estimate_list']['available'] = repairer.repairs_cuckoos
                        elif str(self.object.clock_type_fk) == 'Atmospheric':
                            context['estimate_list']['available'] = repairer.repairs_atmospherics
                        elif str(self.object.clock_type_fk) == 'Anniversary':
                            context['estimate_list']['available'] = repairer.repairs_anniversarys
                        elif self.object.drive_type == 'Quartz':
                            context['estimate_list']['available'] = repairer.repairs_most_quartz
                            extra_features -= 2
                        else:
                            context['estimate_list']['available'] = repairer.repairs_most_mechanical

                        est_debug_text += 'Available ' + str(context['estimate_list']['available']) + '\n'

                        # Exit loop if repairer is not available...
                        # if context['estimate_list']['available'] != True:
                        #     break

                        # Check for extra drive time...
                        if double_repairer_round_trip_included < double_round_trip_minutes:
                            est_hours += (double_round_trip_minutes - double_repairer_round_trip_included) / 60
                        else:
                            est_debug_text += 'No extra road time: ' + str(double_repairer_round_trip_included) + ' < ' + str(double_round_trip_minutes) + ' | hours(' + str(round(est_hours,2)) + ')\n'

                        # Check for extra features...
                        # Wooden gears
                        if self.object.gear_material == 'Wood':
                            context['estimate_list']['available'] = repairer.repairs_most_mechanical
                            extra_features += 2
                        else:
                            est_debug_text += self.object.gear_material + ' != Wood | hours(' + str(round(est_hours,2)) + ')\n'
                        # Not self-adjusting strike
                        if self.object.has_self_adjusting_strike == False:
                            extra_features += 1
                        else:
                            est_debug_text += 'Has self adjusting strike: ' + str(self.object.has_self_adjusting_strike) + ' != False | hours(' + str(round(est_hours,2)) + ')\n'
                        # Has off-at-night
                        if self.object.has_off_at_night:
                            extra_features += 0.5
                        else:
                            est_debug_text += 'Has off-at-night: ' + str(self.object.has_off_at_night) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
                        # Has calendar
                        if self.object.has_calendar:
                            extra_features += 0.5
                        else:
                            est_debug_text += 'Has calendar: ' + str(self.object.has_calendar) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
                        # Has moon dial
                        if self.object.has_moon_dial:
                            extra_features += 0.25
                        else:
                            est_debug_text += 'Has moon dial: ' + str(self.object.has_moon_dial) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
                        # Has alarm
                        if self.object.has_alarm:
                            extra_features += 1
                        else:
                            est_debug_text += 'Has alarm: ' + str(self.object.has_alarm) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
                        # Has music box
                        if self.object.has_music_box:
                            extra_features += 1.5
                        else:
                            est_debug_text += 'Has music box: ' + str(self.object.has_music_box) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
                        # Has activity other
                        if self.object.has_activity_other:
                            extra_features += 1
                        else:
                            est_debug_text += 'Has activity other: ' + str(self.object.has_activity_other) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'
                        # Five tubes included in the price
                        if self.object.tube_count >= 5:
                            extra_features += 0.50
                        else:
                            est_debug_text += 'tube_count: ' + str(self.object.tube_count) + ' < 6\n'

                        # Check for Cable or String...
                        if self.object.drive_type == 'Cable' or self.object.drive_type == 'String':
                            est_hours += 1.5
                        else:
                            est_debug_text += self.object.drive_type + ' != Cable or' + self.object.drive_type + ' != String | hours(' + str(round(est_hours,2)) + ')\n'
                        # Check if Tubular...
                        if self.object.has_tubes:
                            context['estimate_list']['available'] = repairer.repairs_tubular_grandfathers
                            est_hours += 5
                        else:
                            est_debug_text += 'Has tubes: ' + str(self.object.has_tubes) + ' != True | hours(' + str(round(est_hours,2)) + ')\n'

                        est_debug_text += 'extras: ' + str(extra_features) + ' | hours(' + str(round(est_hours,2)) + ')\n'

                        est_hours += (extra_features * 0.50)
                    else:
                        context['estimate_list']['available'] = False
                        est_debug_text += 'Accepting Jobs (' + str(repairer.still_accepting_jobs) + ') and ' + str(double_round_trip_minutes) + ' <= ' + str(repairer.road_time_minutes_maximum) + ' | hours(' + str(round(est_hours,2)) + ')\n'

                    context['estimate_list']['hours'] = est_hours
                    context['estimate_list']['est_hours'] = math.ceil((est_hours * float(repairer.hourly_rate)))
                    context['estimate_list']['debug'] = est_debug_text
                    context['estimate_list'].push()
                    repairer_count += 1

                return context
            except:
                return context


