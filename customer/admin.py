from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Customer
# from django.forms import ModelForm
# from floppyforms.gis import PointWidget, BaseGMapWidget

# class CustomPointWidget(PointWidget, BaseGMapWidget):
#     class Media:
#         js = ('/static/floppyforms/js/MapWidget.js',)

# class CustomerAdminForm(ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['first_name', 'location']
#         widgets = {
#             'location': CustomPointWidget()
#         }

# class CustomerAdmin(admin.ModelAdmin):
#     form = CustomerAdminForm

#class CustomerAdmin(admin.ModelAdmin):
class CustomerAdmin(OSMGeoAdmin):
    list_display = ('user_fk', 'user_fk_id', 'first_name', 'last_name', 'location')
    date_hierarchy = 'date_created'

admin.site.register(Customer, CustomerAdmin)
#admin.site.register(Customer)
