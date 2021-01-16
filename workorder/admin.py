from django.contrib import admin
from .models import Workorder

class WorkorderAdmin(admin.ModelAdmin):
    list_display = ('customer_fk', 'clock_fk', 'repairer_fk', 'dynamic_estimate','date_created')
    date_hierarchy = 'date_created'

admin.site.register(Workorder, WorkorderAdmin)
