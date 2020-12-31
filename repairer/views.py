from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Repairer

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
    fields = '__all__'
    context_object_name = 'repairer_create'
    template_name = 'repairer/create.html'

    def form_valid(self, form):
        form.instance.user_fk= self.request.user
        return super().form_valid(form)

class RepairerUpdateView(UpdateView):
    model = Repairer
    fields = '__all__'
    context_object_name = 'repairer_update'
    template_name = 'repairer/update.html'
