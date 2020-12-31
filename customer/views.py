from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Customer

class CustomerListView(ListView):
#    model = Customer
#    queryset = Customer.objects.filter(user_fk_id__exact=request.user)
#    queryset = Customer.objects.filter(user_fk_id__exact=7)
#    queryset = Customer.objects.filter(last_name__exact='Three')
    context_object_name = 'customers'
    template_name = 'customer/customers.html'

    def get_queryset(self):
        if self.request.user:
            return Customer.objects.filter(user_fk_id__exact=self.request.user)
        else:
            return Customer.objects.all()

class CustomerDetailView(DetailView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'customer/customer.html'

# Form Views 
class CustomerCreateView(CreateView):
    model = Customer
    fields = '__all__'
    context_object_name = 'customer_create'
    template_name = 'customer/create.html'

    def form_valid(self, form):
        form.instance.user_fk= self.request.user
        return super().form_valid(form)

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = '__all__'
    context_object_name = 'customer_update'
    template_name = 'customer/update.html'
#    success_url = reverse_lazy('customer')
#    success_url = reverse('customer', kwargs={'pk': model.pk})

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