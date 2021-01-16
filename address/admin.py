from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Address

class AddressAdmin(OSMGeoAdmin):
    list_display = ('user_fk', 'user_fk_id', 'contact_name', 'location')
    date_hierarchy = 'date_created'

admin.site.register(Address, AddressAdmin)
