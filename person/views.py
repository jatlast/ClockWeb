from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template import Context
from django.urls import reverse
from .models import Person
from customer.models import Customer
import traceback

person_fields_viewable_by_everyone = [
        # 'id',
        # 'user_fk',
        # 'date_created',
        'first_name',
        'last_name',
        'phone',
        'account_type',
    ]

#########################
# For Debugging forms #
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# @method_decorator(csrf_exempt, name='dispatch')
#########################
class PersonCreateView(CreateView):
    model = Person
    fields = person_fields_viewable_by_everyone
    context_object_name = 'person'
    template_name = 'person/create.html'

    def form_valid(self, form):
        form.instance.user_fk = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.id
        person = Person.objects.get(id=pk)
        if person.account_type == 'Customer':
           Customer.objects.get_or_create(person_fk_id=pk)
        return reverse("person", kwargs={"pk": pk})


class PersonDetailView(DetailView):
    model = Person
    context_object_name = 'person'
    template_name = 'person/person.html'

class PersonUpdateView(UpdateView):
    model = Person
    fields = person_fields_viewable_by_everyone
    context_object_name = 'person_update'
    template_name = 'person/update.html'

class PersonListView(ListView):
#    model = Person
    context_object_name = 'persons'
    template_name = 'person/persons.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        try:
            return Person.objects.filter(user_fk_id__exact=self.request.user)
        except:
            return None

