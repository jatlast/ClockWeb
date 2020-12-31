from django.contrib import admin
from .models import Clock

class ClockAdmin(admin.ModelAdmin):
    list_display = ("user_fk", "user_fk_id", "clock_type_fk", "footprint", "train_count",)

admin.site.register(Clock, ClockAdmin)

