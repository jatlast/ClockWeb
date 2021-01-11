from django.shortcuts import render
from django.views.generic import CreateView , ListView, DetailView #, UpdateView, DeleteView
from .models import Workorder
from clock.models import Clock
from django.views.decorators.csrf import csrf_exempt
from django.template import Context


workorder_fields_viewable_by_everyone = [
#        'user_fk',
        'clock_fk',
        'repairer_fk',
        'repairer_hourly_rate',
#        'date_created',
        'repair_type',
        'repair_status',
        'repair_description',
        'distance_from_repairer',
        'dynamic_estimate',
        'dynamic_estimate_hours',
        'repairer_estimate_hours',
        'repairer_accepted',
        'repairer_declined',
        'start_date',
        'finish_date',
        'date_paid',
        'total_cost',
    ]

class WorkorderListView(ListView):
#    model = Workorder
    context_object_name = 'workorders'
    template_name = 'workorders/workorders.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None

        try:
            return Workorder.objects.filter(user_fk_id__exact=self.request.user)
        except:
            return None


#########################
# For Debugging forms #
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
#########################
class WorkorderCreateView(CreateView):
    model = Workorder
    fields = workorder_fields_viewable_by_everyone
    context_object_name = 'workorder_add'
    template_name = 'workorders/add.html'

    def form_valid(self, form):
        form.instance.user_fk = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        try:
#            workorder = Workorder.objects.filter(user_fk_id__exact=self.request.user)
#            context = super().get_context_data(**kwargs)
            context = super(WorkorderCreateView, self).get_context_data(**kwargs)

            context['form_variables'] = Context({"foo": "bar"})
            context['form_variables']['repairer_hourly_rate_0'] = self.request.POST.get('repairer_hourly_rate_0', 'Empty')
            context['form_variables']['repairer_hourly_rate_1'] = self.request.POST.get('repairer_hourly_rate_1', 'Empty')
            context['form_variables']['dynamic_estimate_0'] = self.request.POST.get('dynamic_estimate_0', 'Empty')
            context['form_variables']['dynamic_estimate_1'] = self.request.POST.get('dynamic_estimate_1', 'Empty')

            return context
        except:
            return context


class WorkorderDetailView(DetailView):
    model = Workorder
    context_object_name = 'workorder'
    template_name = 'workorders/workorder.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        else:
            context = super(WorkorderDetailView, self).get_context_data(**kwargs)
            context['debug'] = Context({"foo": "bar"})
            context['debug']['clock_fk_id'] = context['workorder'].clock_fk_id
            context['debug']['repairer_fk_id'] = context['workorder'].repairer_fk_id
            try:
                context['clock_list'] = Clock.objects.filter(id__exact=context['workorder'].clock_fk_id)
                return context
            except:
                return context


# Old Code

# workorder_add

#     <h5>The estimate of  $<span id="span_dynamic_estimate"></span> is for {{ form.repair_type }}</h5>

#     <span id="span_distance_from_repairer"></span>

#     <script language="javascript" type="text/javascript">
#         document.getElementById("span_distance_from_repairer").innerHTML = Number(document.getElementById("id_distance_from_repairer").value).toFixed(2);
#         document.getElementById("span_dynamic_estimate").innerHTML = document.getElementById("id_dynamic_estimate").value;
#     </script>
