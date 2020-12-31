from django.contrib import admin
from .models import Clocktype

class ClocktypeAdmin(admin.ModelAdmin):
    list_display = ("clock_type", "footprint", "train_count",)

admin.site.register(Clocktype, ClocktypeAdmin)

