from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_fk', 'user_fk_id', 'first_name', 'last_name', 'phone_number')
    date_hierarchy = 'date_created'

admin.site.register(Customer, CustomerAdmin)
#admin.site.register(Customer)
