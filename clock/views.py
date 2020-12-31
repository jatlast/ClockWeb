from django.views.generic import ListView, DetailView, CreateView, UpdateView #, DeleteView
from .models import Clock

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
    fields = '__all__'
    context_object_name = 'clock_add'
    template_name = 'clocks/add.html'

    def form_valid(self, form):
        form.instance.user_fk= self.request.user
        return super().form_valid(form)

class ClockUpdateView(UpdateView):
    model = Clock
    fields = '__all__'
    context_object_name = 'clock_update'
    template_name = 'clocks/update.html'
