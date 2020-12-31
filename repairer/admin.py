from django.contrib import admin
from .models import Repairer

class RepairerAdmin(admin.ModelAdmin):
    list_display = ('user_fk', 'user_fk_id', 'first_name', 'last_name', 'phone_number')
    date_hierarchy = 'date_created'

admin.site.register(Repairer, RepairerAdmin)
#admin.site.register(Repairer)
