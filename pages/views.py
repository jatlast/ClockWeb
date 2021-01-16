from django.views.generic import TemplateView
from clock.models import Clock
from customer.models import Customer
from repairer.models import Repairer
from django.template import Context

class HomePageView(TemplateView):
    context_object_name = 'home'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return None
        else:
            context = super(HomePageView, self).get_context_data(**kwargs)
            context['debug'] = Context({"foo": "bar"})

            context['customers'] = Customer.objects.filter(user_fk_id__exact=self.request.user)
            context['repairers'] = Repairer.objects.filter(user_fk_id__exact=self.request.user)

            if context['customers'].count() > 0:
                context['clocks'] = Clock.objects.filter(customer_fk__exact=context['customers'][0].id)
            # context['debug']['clock_fk_id'] = context['workorder'].clock_fk_id
            # context['debug']['repairer_fk_id'] = context['workorder'].repairer_fk_id
            return context

class AboutPageView(TemplateView):
    template_name = 'about.html'