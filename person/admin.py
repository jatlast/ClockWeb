from django.contrib import admin
from .models import Person

class PersonAdmin(admin.ModelAdmin):
    list_display = ('user_fk', 'user_fk_id', 'first_name', 'last_name', 'account_type')
    date_hierarchy = 'date_created'

admin.site.register(Person, PersonAdmin)
