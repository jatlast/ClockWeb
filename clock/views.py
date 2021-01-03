from django.views.generic import ListView, DetailView, CreateView, UpdateView #, DeleteView
from django.contrib.gis.db.models.functions import Distance
from .models import Clock
from customer.models import Customer
from repairer.models import Repairer
from django.template import Context

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
        if self.request.user:
            return Clock.objects.filter(user_fk_id__exact=self.request.user)
        else:
            return Clock.objects.all()

class ClockDetailView(DetailView):
    model = Clock
    context_object_name = 'clock'
    template_name = 'clocks/clock.html'

class ClockCreateView(CreateView):
    model = Clock
    fields = clock_fields_viewable_by_everyone
    context_object_name = 'clock_add'
    template_name = 'clocks/add.html'

    def form_valid(self, form):
        form.instance.user_fk= self.request.user
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
        context = super(ClockRepairEstimateView, self).get_context_data(**kwargs)
        context['customer_list'] = Customer.objects.filter(user_fk_id__exact=self.request.user)
        context['repairer_list'] = Repairer.objects.annotate(distance=Distance('location', context['customer_list'][0].location)).order_by('distance')[0:5]

        context['estimate_list'] =  Context({"foo": "bar"})

        repairer_count = 0
        for repairer in context['repairer_list']:
            context['estimate_list']['id'] = repairer.id
            context['estimate_list']['clock_id'] = self.object.clock_type_fk
            context['estimate_list']['debug'] = '\n'
            # Begin clock repair estimation logic...
            #   convert distance to road time in minutes: miles / mph * 60
            mph = 45 # assuming 45 mph because distance is "as the crow flies" so as not to use direction software
            minutes = 60 # obvious
            miles_to_minutes_multiple = mph / minutes
            round_trip_minutes = (repairer.distance.mi * miles_to_minutes_multiple * 2)
            extra_features = 0 # keep track of GF extra features
            extra_road_time = 0.0
            # check if repairer is accepting jobs and is within the maximum drive time.
            if repairer.still_accepting_jobs and round_trip_minutes <= repairer.road_time_maximum:
                context['estimate_list']['debug'] += 'Accepting Jobs\n'
                
                # begin by setting minimum repair cost
                context['estimate_list']['estimate'] = repairer.repair_minimum

                # Check for extra drive time...
                if repairer.road_time_included < round_trip_minutes:
                    extra_road_time += (round_trip_minutes - repairer.road_time_included) * round_trip_minutes
                else:
                    context['estimate_list']['debug'] += 'No extra road time: ' + str(repairer.road_time_included) + ' < ' + str(round_trip_minutes) + '\n'

                # Wooden gears
                if self.object.gear_material == 'Wood':
                    extra_features += 1
                else:
                    context['estimate_list']['debug'] += self.object.gear_material + ' != Wood\n'
                # Check for extra features...
                # Wooden gears
                if self.object.gear_material == 'Wood':
                    extra_features += 1
                else:
                    context['estimate_list']['debug'] += self.object.gear_material + ' != Wood\n'
                # Not self-adjusting strike
                if self.object.has_self_adjusting_strike == False:
                    extra_features += 1
                else:
                    context['estimate_list']['debug'] += 'Has self adjusting strike: ' + str(self.object.has_self_adjusting_strike) + ' != False\n'
                # Has off-at-night
                if self.object.has_off_at_night:
                    extra_features += 1
                else:
                    context['estimate_list']['debug'] += 'Has off-at-night: ' + str(self.object.has_off_at_night) + ' != True\n'
                # Has calendar
                if self.object.has_calendar:
                    extra_features += 1
                else:
                    context['estimate_list']['debug'] += 'Has calendar: ' + str(self.object.has_calendar) + ' != True\n'
                # Has moon dial
                if self.object.has_moon_dial:
                    extra_features += 1
                else:
                    context['estimate_list']['debug'] += 'Has moon dial: ' + str(self.object.has_moon_dial) + ' != True\n'
                # Has alarm
                if self.object.has_alarm:
                    extra_features += 1
                else:
                    context['estimate_list']['debug'] += 'Has alarm: ' + str(self.object.has_alarm) + ' != True\n'
                # Has music box
                if self.object.has_music_box:
                    extra_features += 1
                else:
                    context['estimate_list']['debug'] += 'Has music box: ' + str(self.object.has_music_box) + ' != True\n'
                # Has activity other
                if self.object.has_activity_other:
                    extra_features += 1
                else:
                    context['estimate_list']['debug'] += 'Has activity other: ' + str(self.object.has_activity_other) + ' != True\n'
                # Five tubes included in the price
                if self.object.tube_count >= 5:
                    extra_features += 1
                else:
                    context['estimate_list']['debug'] += 'tube_count: ' + str(self.object.tube_count) + ' < 6\n'

                context['estimate_list']['debug'] += 'extras: ' + str(extra_features) + '\n'

                # Check for specific clock_type...
                clock_type = 'Longcase/Grandfather'
                if str(self.object.clock_type_fk) == clock_type:
                    context['estimate_list']['debug'] += 'clock_type: ' + clock_type + '\n'
                    # GF chain drives are the least expensive
                    context['estimate_list']['estimate'] = repairer.repair_gf_chain
                    # Check for Cable or String...
                    if self.object.drive_type == 'Cable' or self.object.drive_type == 'String':
                        context['estimate_list']['estimate'] = repairer.repair_gf_cable
                    else:
                        context['estimate_list']['debug'] += self.object.drive_type + ' != Cable or' + self.object.drive_type + ' != String\n'
                    # Check if Tubular...
                    if self.object.has_tubes:
                        context['estimate_list']['estimate'] = repairer.repair_gf_tubular
                    else:
                        context['estimate_list']['debug'] += 'Has tubes: ' + str(self.object.has_tubes) + ' != True\n'
                    if extra_features > 0:
                        original_estimate = context['estimate_list']['estimate']
                        context['estimate_list']['estimate'] += (extra_features * original_estimate * repairer.multiple_per_gf_extra)
                        context['estimate_list']['debug'] += 'extras: ' + str(original_estimate) + ' += (' + str(extra_features) + ' * ' +  str(original_estimate) + ' * ' + str(repairer.multiple_per_gf_extra) + ' = ' + str(context['estimate_list']['estimate']) + '\n'
                    else:
                        context['estimate_list']['debug'] += str(extra_features) + ' <= 0\n'
                else:
                    context['estimate_list']['debug'] += str(self.object.clock_type_fk) + ' != ' + clock_type + '\n'
            else:
                context['estimate_list']['debug'] += 'Accepting Jobs (' + str(repairer.still_accepting_jobs) + ') and ' + str(round_trip_minutes) + ' <= ' + str(repairer.road_time_maximum) + '\n'

            context['estimate_list'].push()
            repairer_count += 1

        return context


