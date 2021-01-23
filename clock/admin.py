from django.contrib import admin
from .models import Clock, Clocktypes

# class ReviewInline(admin.TabularInline):
#     model = Review

class ClocktypesAdmin(admin.ModelAdmin):
    list_display = ('id','clock_type', 'footprint', 'train_count', 'chime_count', 'tube_count', 'battery_count',)

class ClockAdmin(admin.ModelAdmin):
    list_display = ('customer_fk', 'clock_type_fk', 'footprint', 'train_count',)

admin.site.register(Clocktypes, ClocktypesAdmin)
admin.site.register(Clock, ClockAdmin)

