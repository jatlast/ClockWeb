from django.views.generic import TemplateView
from person.models import Person
from address.models import Address
from customer.models import Customer
from repairer.models import Repairer
#from clock.models import Clock
from django.template import Context
import traceback

class HomePageView(TemplateView):
    context_object_name = 'home'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        try:
            context = super(HomePageView, self).get_context_data(**kwargs)
            context['debug'] = Context({"foo": "bar"})

            context['person'] = Person.objects.get(user_fk_id__exact=self.request.user)

            if context['person'].account_type == 'Customer':
                context['customer'] = Customer.objects.get(person_fk_id__exact=context['person'].id)
#                context['clocks'] = Clock.objects.filter(customer_fk__exact=context['customer'].id)
            elif context['person'].account_type == 'Repairer':
                context['repairer'] = Repairer.objects.get(person_fk_id__exact=context['person'].id)

            return context
        except Exception as e:
            trace_back = traceback.format_exc()
            context['debug']['exception'] = str(e) + " " + str(trace_back)
            return context

class AboutPageView(TemplateView):
    template_name = 'about.html'