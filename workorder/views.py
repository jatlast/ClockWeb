from django.shortcuts import render
from django.views.generic import CreateView , ListView, DetailView #, UpdateView, DeleteView
from .models import Workorder, Addons
from clock.models import Clock
from customer.models import Customer
from repairer.models import Repairer
from django.template import Context
from django.urls import reverse
from datetime import datetime
import traceback

workorder_fields_viewable_by_everyone = [
#        'user_fk',
        'clock_fk',
        'repairer_fk',
        'repairer_hourly_rate',
#        'date_created',
#        'date_last_updated'
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

class WorkorderCustomerListView(ListView):
    context_object_name = 'workorders'
    template_name = 'customer/workorders.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        try:
            return Workorder.objects.filter(user_fk_id__exact=self.request.user).order_by('-date_last_updated')
        except:
            return None

class WorkorderRepairerListView(ListView):
    context_object_name = 'workorders'
    template_name = 'repairer/workorders.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None

        repairer_fk_id = Repairer.objects.only('id').get(user_fk_id=self.request.user).id
        return Workorder.objects.filter(repairer_fk_id__exact=repairer_fk_id).order_by('-date_last_updated')
        # try:
        #     return Workorder.objects.filter(repairer_fk_id__exact=repairer_fk_id).order_by('-date_last_updated')
        # except:
        #     return None


#########################
# For Debugging forms #
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
#########################
class WorkorderCreateView(CreateView):
    model = Workorder
    fields = workorder_fields_viewable_by_everyone
    context_object_name = 'workorder_add'
    template_name = 'workorders/add.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        try:
#            workorder = Workorder.objects.filter(user_fk_id__exact=self.request.user)
#            context = super().get_context_data(**kwargs)
            context = super(WorkorderCreateView, self).get_context_data(**kwargs)

            context['form_variables'] = Context({"foo": "bar"})
            # Required params for passing the two parts that make up MoneyField variables
            context['form_variables']['repairer_hourly_rate_0'] = self.request.POST.get('repairer_hourly_rate_0', 'Empty')
            context['form_variables']['repairer_hourly_rate_1'] = self.request.POST.get('repairer_hourly_rate_1', 'Empty')
            context['form_variables']['dynamic_estimate_0'] = self.request.POST.get('dynamic_estimate_0', 'Empty')
            context['form_variables']['dynamic_estimate_1'] = self.request.POST.get('dynamic_estimate_1', 'Empty')
            return context
        except:
            return context

    def form_valid(self, form):
        form.instance.user_fk = self.request.user
        form.instance.customer_fk_id = Customer.objects.only('id').get(user_fk_id=self.request.user).id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("customer_workorder", args=(self.object.id,))


class WorkorderDetailCustomerView(DetailView):
    model = Workorder
    context_object_name = 'workorder'
    template_name = 'customer/workorder.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        else:
            context = super(WorkorderDetailCustomerView, self).get_context_data(**kwargs)
            context['debug'] = Context({"foo": "bar"})
            context['debug']['clock_fk_id'] = context['workorder'].clock_fk_id
            context['debug']['repairer_fk_id'] = context['workorder'].repairer_fk_id
            try:
                context['customer'] = Customer.objects.get(user_fk_id=self.request.user)
                context['clock'] = Clock.objects.get(id=context['workorder'].clock_fk_id)
                context['repairer'] = Repairer.objects.get(id=context['workorder'].repairer_fk_id)
                context['repairer']['repairer_estimate'] = context['workorder'].repairer_estimate_hours * context['workorder'].repairer_hourly_rate
                return context
            except Exception as e:
                trace_back = traceback.format_exc()
                context['debug']['exception'] = str(e) + " " + str(trace_back)
                return context

class WorkorderDetailRepairerView(DetailView):
#    model = Workorder
    context_object_name = 'workorder'
    template_name = 'repairer/workorder.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        pk = self.kwargs["pk"]
        repairer_fk_id = Repairer.objects.only('id').get(user_fk_id=self.request.user).id
        return Workorder.objects.filter(id__exact=pk).filter(repairer_fk_id__exact=repairer_fk_id)

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        else:
            context = super(WorkorderDetailRepairerView, self).get_context_data(**kwargs)
            context['debug'] = Context({"foo": "bar"})
            context['debug']['clock_fk_id'] = context['workorder'].clock_fk_id
            context['debug']['repairer_fk_id'] = context['workorder'].repairer_fk_id
            try:
                context['customer'] = Customer.objects.get(id=context['workorder'].customer_fk_id)
                context['clock'] = Clock.objects.get(id=context['workorder'].clock_fk_id)
                context['repairer'] = Repairer.objects.get(id=context['workorder'].repairer_fk_id)
                context['debug']['repairer_estimate'] = context['workorder'].repairer_estimate_hours * context['workorder'].repairer_hourly_rate
                context['addons'] = Addons.objects.filter(workorder_fk__exact=context['workorder'].id).order_by('date_created')
                return context
            except Exception as e:
                trace_back = traceback.format_exc()
                context['debug']['exception'] = str(e) + " " + str(trace_back)
                return context

addons_fields_viewable_by_everyone = [
#        'id',
        'workorder_fk',
#        'date_created',
#        'added_by',
        'addon_type',
#        'repair_status_previous',
        'repair_status_update',
        'addon_description',
        'added_hours',
        'added_part_cost',
        'override_part_cost_multiple',
        'image_1',
        'image_2',
        'image_3',
        'image_4',
        'image_5',
    ]

@method_decorator(csrf_exempt, name='dispatch')
class AddonsCreateRepairerView(CreateView):
    model = Addons
    fields = addons_fields_viewable_by_everyone
    context_object_name = 'addons'
    template_name = 'repairer/addons_add.html'

    # def get_context_data(self, **kwargs):
    #     if not self.request.user.is_authenticated:
    #         return None
    #     else:
    #         context = super(AddonsCreateRepairerView, self).get_context_data(**kwargs)
    #         context['debug'] = Context({"foo": "bar"})
    #         try:
    #             workorder_fk = self.request.POST.get('workorder_fk', 'PostGetError')
    #             context['workorder'] = Workorder.objects.get(id=workorder_fk)
    #             return context
    #         except Exception as e:
    #             trace_back = traceback.format_exc()
    #             context['debug']['exception'] = str(e) + " " + str(trace_back)
    #             return context

    # def form_valid(self, form):
    #     workorder_fk = self.request.POST.get('workorder_fk', 'PostGetError')
    #     repair_status_previous = Workorder.objects.only('repair_status').get(id=workorder_fk).repair_status
    #     form.instance.repair_status_previous = repair_status_previous
    #     form.instance.added_by = 'Repairer'
    #     return super().form_valid(form)

    def get_success_url(self):
#        pk = self.kwargs["pk"]
        pk = self.object.id
        addon = Addons.objects.get(id=pk)
        # Update the relevant Workorder based on Addon's workorder_fk...
        workorder_fk = self.request.POST.get('workorder_fk', 'PostGetError')
        workorder = Workorder.objects.get(id=workorder_fk)
        workorder.date_last_updated = datetime.now()
        addon.added_by = 'Repairer'
        addon.repair_status_previous = workorder.repair_status
        addon.save()
        workorder.repair_status = self.request.POST.get('repair_status_update', 'PostGetError')
        workorder.save()
        return reverse("repairer_workorder", kwargs={"pk": workorder_fk})

# Old Code

# workorder_add

#     <h5>The estimate of  $<span id="span_dynamic_estimate"></span> is for {{ form.repair_type }}</h5>

#     <span id="span_distance_from_repairer"></span>

#     <script language="javascript" type="text/javascript">
#         document.getElementById("span_distance_from_repairer").innerHTML = Number(document.getElementById("id_distance_from_repairer").value).toFixed(2);
#         document.getElementById("span_dynamic_estimate").innerHTML = document.getElementById("id_dynamic_estimate").value;
#     </script>

                            # <td class="title">
                            #     <img src="{% static 'images/logo.png' %}" style="width:50%; max-width:300px;">
                            # </td>                            
