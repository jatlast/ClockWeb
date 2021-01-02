from django.views.generic import ListView, DetailView, CreateView, UpdateView #, DeleteView
from .models import Clock

clock_fields_viewable_by_everyone = [
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
