from django.views.generic import TemplateView
from clock.models import Clock
from customer.models import Customer
from repairer.models import Repairer
from address.models import Address
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
            context['addresses'] = Address.objects.filter(user_fk_id__exact=self.request.user)

            if context['customers'].count() > 0:
                context['clocks'] = Clock.objects.filter(customer_fk__exact=context['customers'][0].id)

            return context

class AboutPageView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        context['debug'] = Context({"foo": "bar"})

        context['repairer'] = Repairer.objects.get(first_name__exact='Jason', last_name__exact='Baumbach')

        return context

class PageWalkthroughCustomerView(TemplateView):
    template_name = 'cwt.html'
    # template_name = 'customer-walkthrough.html'

class PageWalkthroughRepairerView(TemplateView):
    template_name = 'rwt.html'
    # template_name = 'clock-repair-person-walkthrough.html'
