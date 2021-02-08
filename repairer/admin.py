from django.contrib import admin
from .models import Repairer

class RepairerAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'user_fk', 'user_fk_id', 'first_name', 'last_name', 'hourly_rate',)
    date_hierarchy = 'date_created'

    # def form_valid(self, form):
    #     longitude = form.cleaned_data['longitude']
    #     latitude = form.cleaned_data['latitude']
    #     form.instance.location = Point(longitude, latitude, srid=4326)
    #     return super().form_valid(form)

admin.site.register(Repairer, RepairerAdmin)
#admin.site.register(Repairer)
