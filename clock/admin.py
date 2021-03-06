from django.contrib import admin
from .models import Clock, Clocktypes

# class ReviewInline(admin.TabularInline):
#     model = Review

class ClocktypesAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'id','clock_type', 'footprint', 'wind_interval_days', 'train_count', 'chime_count', 'tube_count', 'battery_count',)

class ClockAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'customer_fk', 'clock_type_fk', 'footprint', 'train_count',)

admin.site.register(Clocktypes, ClocktypesAdmin)
admin.site.register(Clock, ClockAdmin)

