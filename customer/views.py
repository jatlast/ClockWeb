from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Customer
from repairer.models import Repairer
#from clock.models import Clock
from django.template import Context
# Decorators to force users to be logged in to access the different Views.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

customer_fields_viewable_by_everyone = [
        'first_name',
        'last_name',
        'phone',
]

@method_decorator(login_required, name='dispatch')
class CustomerListView(ListView):
    model = Customer
    context_object_name = 'customers'
    template_name = 'customer/customers.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        else:
            context = super(CustomerListView, self).get_context_data(**kwargs)
            context['customers'] = Customer.objects.filter(user_fk_id__exact=self.request.user)
            return context


@method_decorator(login_required, name='dispatch')
class CustomerCreateView(CreateView):
    model = Customer
    fields = customer_fields_viewable_by_everyone
    context_object_name = 'customer_create'
    template_name = 'customer/create.html'
    success_url='/customers'

    def form_valid(self, form):
        form.instance.user_fk = self.request.user
        response = super().form_valid(form)
        response.set_cookie('user_type', 'customer', 3600 * 24 * 365 * 2) # = 63,072,000 seconds = 2 years
        return response

@method_decorator(login_required, name='dispatch')
class CustomerUpdateView(UpdateView):
    model = Customer
    fields = customer_fields_viewable_by_everyone
    context_object_name = 'customer_update'
    template_name = 'customer/update.html'
    success_url='/customers'

    def form_valid(self, form):
        response = super().form_valid(form)
        response.set_cookie('user_type', 'customer', 3600 * 24 * 365 * 2) # = 63,072,000 seconds = 2 years
        return response

@method_decorator(login_required, name='dispatch')
class RepairersNearMeView(ListView):
    context_object_name = 'customers'
    template_name = 'customer/nearme.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        try:
            customer = Customer.objects.filter(user_fk_id__exact=self.request.user)

            context = super(RepairersNearMeView, self).get_context_data(**kwargs)
            context['repairer_list'] = Repairer.objects.annotate(distance=Distance('location', customer[0].location)).order_by('distance')[0:5]

            context['estimate_list'] =  Context({"foo": "bar"})

            repairer_count = 0
            for repairer in context['repairer_list']:
                context['estimate_list']['id'] = repairer.id
                context['estimate_list']['dist'] = repairer.distance.mi
                context['estimate_list'].push()
                repairer_count += 1

            return context
        except:
            return None


#        events = Event.objects.filter(datetime__gte=now).filter(datetime__lte=next_week).annotate(distance=Distance('venue__location', location)).order_by('distance')[0:5]


#    new_uuid = str(uuid.uuid4())

    # context ={} 
    # context['form']= CreateCustomerForm() 
    # render(model, "customer/customer_create.html", context)

# class update_customer_form(request, pk):
#     customer_instance = get_object_or_404(Customer, pk=pk)

#     # If this is a POST request then process the Form data
#     if request.method == 'POST':

#         # Create a form instance and populate it with data from the request (binding):
#         form = UpdateCustomerForm(request.POST)

#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             customer_instance.phone_number = form.cleaned_data['phone_number']
#             customer_instance.save()

#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('customer_detail') )

#     # If this is a GET (or any other method) create the default form.
#     else:
#         model = Customer
#         form = UpdateCustomerForm(initial={'renewal_date': model.phone_number})

#     context = {
#         'form': form,
#         'customer_instance': customer_instance,
#     }

#     return render(request, 'customer/customer_detail.html', context)