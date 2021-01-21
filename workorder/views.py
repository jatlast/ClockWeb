from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView #, UpdateView
from .models import Workorder, Addons
from clock.models import Clock
from customer.models import Customer
from repairer.models import Repairer
from address.models import Address
from django.template import Context
from django.urls import reverse
from datetime import datetime
import traceback
import math

# Decorators to force users to be logged in to access the different Views.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

workorder_fields_viewable_by_everyone = [
#        'id',
        'customer_fk',
        'clock_fk',
        'repairer_fk',
        'address_clock_fk',
        'address_deliver_fk',
        'repairer_hourly_rate',
        'repairer_hourly_rate_currency',
#        'date_created',
#        'date_last_updated'
        'repair_type',
        'repair_status',
        'repair_description',
        'distance_from_repairer',
        'dynamic_estimate',
        'dynamic_estimate_hours',
        'total_cost',
    ]


@method_decorator(login_required, name='dispatch')
class WorkorderListView(ListView):
    context_object_name = 'workorders'
    template_name = 'workorders/workorders.html'

    def get_queryset(self):
        user_type_cookie = self.request.COOKIES.get('user_type')
        if user_type_cookie == 'customer':
            # get the current user's customer id from the Customer object
            customer__id = Customer.objects.only('id').get(user_fk_id=self.request.user).id
            return Workorder.objects.filter(customer_fk_id__exact=customer__id).order_by('-date_last_updated')
        elif user_type_cookie == 'repairer':
            # get the current user's repairer id from the Repairer object
            repairer__id = Repairer.objects.only('id').get(user_fk_id=self.request.user).id
            return Workorder.objects.filter(repairer_fk_id__exact=repairer__id).order_by('-date_last_updated')
        else:
            return None

#########################
# For Debugging forms #
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
#########################
#@method_decorator(login_required, name='dispatch')
class WorkorderCreateView(CreateView):
    model = Workorder
    fields = workorder_fields_viewable_by_everyone
    context_object_name = 'workorder_add'
    template_name = 'workorders/add.html'

    # def form_valid(self, form):
    #     dynamic_estimate = self.request.POST.get('dynamic_estimate', '-1')
    #     form.instance.repair_status_previous = dynamic_estimate
    #     form.instance.added_by = 'Repairer'
    #     return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(WorkorderCreateView, self).get_context_data(**kwargs)
    #     context['form_fields'] = Context({"foo": "bar"})
    #     # Required params for passing the two parts that make up MoneyField variables
    #     context['form_fields']['repairer_hourly_rate_0'] = self.request.POST.get('repairer_hourly_rate_0', 'Empty')
    #     context['form_fields']['repairer_hourly_rate_1'] = self.request.POST.get('repairer_hourly_rate_1', 'Empty')
    #     context['form_fields']['dynamic_estimate_0'] = self.request.POST.get('dynamic_estimate_0', 'Empty')
    #     context['form_fields']['dynamic_estimate_1'] = self.request.POST.get('dynamic_estimate_1', 'Empty')
    #     return context

@method_decorator(login_required, name='dispatch')
class WorkorderDeleteView(DeleteView):
    model = Workorder
    template_name = 'workorders/workorder_confirm_delete.html'
    success_url = '/workorders/'

@method_decorator(login_required, name='dispatch')
class WorkorderDetailView(DetailView):
    model = Workorder
    context_object_name = 'workorder'
    template_name = 'workorders/workorder.html'

    def get_context_data(self, **kwargs):
        context = super(WorkorderDetailView, self).get_context_data(**kwargs)
        context['debug'] = Context({"foo": "bar"})

        context['debug']['clock_fk_id'] = context['workorder'].clock_fk_id
        context['debug']['repairer_fk_id'] = context['workorder'].repairer_fk_id
        context['debug']['address_clock_fk_id'] = context['workorder'].address_clock_fk_id
        context['debug']['address_deliver_fk_id'] = context['workorder'].address_deliver_fk_id

        context['clock'] = Clock.objects.get(id=context['workorder'].clock_fk_id)
        context['customer'] = Customer.objects.get(id=context['workorder'].customer_fk_id)
        context['repairer'] = Repairer.objects.get(id=context['workorder'].repairer_fk_id)
        context['address_clock'] = Address.objects.get(id=context['workorder'].address_clock_fk_id)

        repairer__user_fk_id = Repairer.objects.only('id').get(id=context['workorder'].repairer_fk_id).user_fk_id
        context['address_repairer'] = Address.objects.get(user_fk_id__exact=repairer__user_fk_id)

        if context['workorder'].address_deliver_fk_id and context['workorder'].address_clock_fk_id != context['workorder'].address_deliver_fk_id:
            context['address_deliver'] = Address.objects.get(id=context['workorder'].address_deliver_fk_id)

        # context['debug']['repairer_estimate'] = context['workorder'].repairer_estimate_hours * context['workorder'].repairer_hourly_rate
        context['addons'] = Addons.objects.filter(workorder_fk__exact=context['workorder'].id).order_by('date_created')
        return context

        # try:
        #     context['debug']['repairer_estimate'] = context['workorder'].repairer_estimate_hours * context['workorder'].repairer_hourly_rate
        #     context['addons'] = Addons.objects.filter(workorder_fk__exact=context['workorder'].id).order_by('date_created')
        #     return context
        # except Exception as e:
        #     trace_back = traceback.format_exc()
        #     context['debug']['exception'] = str(e) + " " + str(trace_back)
        #     return context



addons_fields_viewable_by_template = [
        # 'id',
        'workorder_fk',
        # 'date_created',
        # 'added_by',
        'addon_type',
        # 'repair_status_previous',
        'repair_status_update',
        'addon_description',
        'added_hours',
        'added_part_cost',
        'part_cost_multiple',
        # 'added_customer_cost',
        'image_1',
        'image_2',
        'image_3',
        'image_4',
        'image_5',
    ]

addons_fields_viewable_by_repairer = [
        # 'id',
        # 'workorder_fk',
        # 'date_created',
        # 'added_by',
        'addon_type',
        # 'repair_status_previous',
        'repair_status_update',
        'addon_description',
        'added_hours',
        'added_part_cost',
        'part_cost_multiple',
        # 'added_customer_cost',
        'image_1',
        'image_2',
        'image_3',
        'image_4',
        'image_5',
    ]

addons_fields_viewable_by_customer = [
        # 'id',
        # 'workorder_fk',
        # 'date_created',
        # 'added_by',
        'addon_type',
        # 'repair_status_previous',
        'repair_status_update',
        'addon_description',
        # 'added_hours',
        # 'added_part_cost',
        # 'part_cost_multiple',
        # 'added_customer_cost',
        'image_1',
        'image_2',
        'image_3',
        'image_4',
        'image_5',
    ]

@method_decorator(csrf_exempt, name='dispatch')
class AddonsCreateView(CreateView):
    model = Addons
    fields = addons_fields_viewable_by_template
    context_object_name = 'addons'
    template_name = 'workorders/addons/add.html'

    # def get_queryset(self):
    #     user_type_cookie = self.request.COOKIES.get('user_type')
    #     if user_type_cookie == 'repairer':
    #         return Addons.objects.filter(user_fk_id__exact=self.request.user).values(*addons_fields_viewable_by_repairer)
    #     else:
    #         return Addons.objects.filter(user_fk_id__exact=self.request.user).values(*addons_fields_viewable_by_customer)
 
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
        addon.user_fk_id = self.request.user
        if addon.added_part_cost:
            addon.added_customer_cost = math.ceil(addon.added_part_cost * addon.part_cost_multiple)
            workorder.total_cost = workorder.total_cost + addon.added_customer_cost
        elif addon.added_hours:
            addon.added_customer_cost = math.ceil(addon.added_hours * workorder.repairer_hourly_rate)
            workorder.total_cost = workorder.total_cost + addon.added_customer_cost
        addon.save()
        workorder.repair_status = self.request.POST.get('repair_status_update', 'PostGetError')
        workorder.save()
        return reverse("workorder", kwargs={"pk": workorder_fk})

    def get_context_data(self, **kwargs):
        context = super(AddonsCreateView, self).get_context_data(**kwargs)
        context['form_fields'] = Context({"foo": "bar"})
        user_type_cookie = self.request.COOKIES.get('user_type')
        if user_type_cookie == 'repairer':
            context['form_fields']['viewable'] = addons_fields_viewable_by_repairer
        else:
            context['form_fields']['viewable'] = addons_fields_viewable_by_customer
        return context

    # def form_valid(self, form):
    #     workorder_fk = self.request.POST.get('workorder_fk', 'PostGetError')
    #     repair_status_previous = Workorder.objects.only('repair_status').get(id=workorder_fk).repair_status
    #     form.instance.repair_status_previous = repair_status_previous
    #     form.instance.added_by = 'Repairer'
    #     return super().form_valid(form)


# Old Code -- Workorders

# class WorkorderCustomerListView(ListView):
#     context_object_name = 'workorders'
#     template_name = 'customer/workorders.html'

#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return None
#         try:
#             return Workorder.objects.filter(user_fk_id__exact=self.request.user).order_by('-date_last_updated')
#         except:
#             return None

# class WorkorderRepairerListView(ListView):
#     context_object_name = 'workorders'
#     template_name = 'repairer/workorders.html'

#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return None

#         repairer_fk_id = Repairer.objects.only('id').get(user_fk_id=self.request.user).id
#         return Workorder.objects.filter(repairer_fk_id__exact=repairer_fk_id).order_by('-date_last_updated')
#         # try:
#         #     return Workorder.objects.filter(repairer_fk_id__exact=repairer_fk_id).order_by('-date_last_updated')
#         # except:
#         #     return None


# class WorkorderDetailCustomerView(DetailView):
#     model = Workorder
#     context_object_name = 'workorder'
#     template_name = 'customer/workorder.html'

#     def get_context_data(self, **kwargs):
#         if not self.request.user.is_authenticated:
#             return None
#         else:
#             context = super(WorkorderDetailCustomerView, self).get_context_data(**kwargs)
#             context['debug'] = Context({"foo": "bar"})
#             context['debug']['clock_fk_id'] = context['workorder'].clock_fk_id
#             context['debug']['repairer_fk_id'] = context['workorder'].repairer_fk_id
#             try:
#                 context['customer'] = Customer.objects.get(user_fk_id=self.request.user)
#                 context['clock'] = Clock.objects.get(id=context['workorder'].clock_fk_id)
#                 context['repairer'] = Repairer.objects.get(id=context['workorder'].repairer_fk_id)
#                 context['repairer']['repairer_estimate'] = context['workorder'].repairer_estimate_hours * context['workorder'].repairer_hourly_rate
#                 return context
#             except Exception as e:
#                 trace_back = traceback.format_exc()
#                 context['debug']['exception'] = str(e) + " " + str(trace_back)
#                 return context

# class WorkorderDetailRepairerView(DetailView):
# #    model = Workorder
#     context_object_name = 'workorder'
#     template_name = 'repairer/workorder.html'

#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return None
#         pk = self.kwargs["pk"]
#         repairer_fk_id = Repairer.objects.only('id').get(user_fk_id=self.request.user).id
#         return Workorder.objects.filter(id__exact=pk).filter(repairer_fk_id__exact=repairer_fk_id)

#     def get_context_data(self, **kwargs):
#         if not self.request.user.is_authenticated:
#             return None
#         else:
#             context = super(WorkorderDetailRepairerView, self).get_context_data(**kwargs)
#             context['debug'] = Context({"foo": "bar"})
#             context['debug']['clock_fk_id'] = context['workorder'].clock_fk_id
#             context['debug']['repairer_fk_id'] = context['workorder'].repairer_fk_id
#             try:
#                 context['customer'] = Customer.objects.get(id=context['workorder'].customer_fk_id)
#                 context['clock'] = Clock.objects.get(id=context['workorder'].clock_fk_id)
#                 context['repairer'] = Repairer.objects.get(id=context['workorder'].repairer_fk_id)
#                 context['debug']['repairer_estimate'] = context['workorder'].repairer_estimate_hours * context['workorder'].repairer_hourly_rate
#                 context['addons'] = Addons.objects.filter(workorder_fk__exact=context['workorder'].id).order_by('date_created')
#                 return context
#             except Exception as e:
#                 trace_back = traceback.format_exc()
#                 context['debug']['exception'] = str(e) + " " + str(trace_back)
#                 return context


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



# Old Code -- Addons
