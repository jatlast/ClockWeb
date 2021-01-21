from django.contrib import admin
from .models import Workorder, Addons

class WorkorderAdmin(admin.ModelAdmin):
    list_display = ('customer_fk', 'clock_fk', 'repairer_fk', 'dynamic_estimate','date_created')
    date_hierarchy = 'date_created'

class AddonsAdmin(admin.ModelAdmin):
    list_display = ('workorder_fk', 'user_fk', 'addon_type', 'repair_status_update','date_created')
    date_hierarchy = 'date_created'

admin.site.register(Workorder, WorkorderAdmin)
admin.site.register(Addons, AddonsAdmin)

