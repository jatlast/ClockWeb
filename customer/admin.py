from django.contrib import admin
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

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('person_fk', 'person_fk_id', 'date_created')
    date_hierarchy = 'date_created'

admin.site.register(Customer, CustomerAdmin)
#admin.site.register(Customer)
