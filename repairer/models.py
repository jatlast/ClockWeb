import uuid
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from djmoney.models.fields import MoneyField
#from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from customer.models import Customer

class Repairer(models.Model):
    FULL_OR_PART_TIME_CHOICES = [
        ('Full','Full Time'),
        ('Part','Part Time'),
    ]

    _CHOICES = [
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
    ]

    # UUID for this table
    id = models.UUIDField(
        primary_key = True
        , default = uuid.uuid4
        , editable = False
    )

    # user_fk - ID from login credentials
    user_fk = models.ForeignKey(
        get_user_model()
        , on_delete = models.CASCADE
#        , editable = False
        , default=1
    )

    # General contact information fields...
    date_created = models.DateTimeField(default=datetime.now, editable=False)
    first_name = models.CharField(blank=False, max_length=16)
    last_name = models.CharField(blank=False, max_length=16)
    company_name = models.CharField(blank=True, max_length=32)
    phone_number = PhoneNumberField(blank=False)
    address_street = models.CharField(blank=False, max_length=32)
    address_other = models.CharField(blank=True, max_length=16)
    city = models.CharField(blank=False, max_length=32)
    state = models.CharField(blank=False, max_length=2, choices=Customer.US_STATE_CHOICES)
    zipcode = models.CharField(blank=False, max_length=32)

    latitude = models.FloatField(default=42.95)
    longitude = models.FloatField(default=-83.64)
    location = models.PointField(blank=False, default=Point(0.0, 0.0), editable=False)

    experience_in_years = models.PositiveSmallIntegerField(blank=False, default=1)
    still_accepting_jobs = models.BooleanField(blank=False, default=True)
    makes_service_calls = models.BooleanField(blank=False, default=False)
    service_call_hours_minimum = models.PositiveSmallIntegerField(blank=False, default=2)
    repairs_grandfathers = models.BooleanField(blank=False, default=False)
    repairs_tubular_grandfathers = models.BooleanField(blank=False, default=False)
    repairs_cuckoos = models.BooleanField(blank=False, default=False)
    repairs_atmospherics = models.BooleanField(blank=False, default=False)
    repairs_anniversarys = models.BooleanField(blank=False, default=False)
    repairs_most_mechanical = models.BooleanField(blank=False, default=False)
    repairs_most_quartz = models.BooleanField(blank=False, default=False)

    # Fields to dynamically determine pricing...
    hourly_rate = MoneyField(max_digits=6, decimal_places=2, blank=False, null=False, default=25.00, default_currency='USD')
#    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=25.00)
    road_time_minutes_included = models.PositiveSmallIntegerField(blank=False, default=15)
    road_time_minutes_maximum = models.PositiveSmallIntegerField(blank=False, default=120)

    multiple_per_part_cost = models.DecimalField(max_digits=3, decimal_places=2, blank=False, default=4.00)
    # commission_percentage = models.DecimalField(max_digits=3, decimal_places=2, blank=False, default=1.00)
    # full_or_part_time = models.CharField(blank=False, max_length=8, choices=FULL_OR_PART_TIME_CHOICES, default='Full')
    # road_time_per_minute = models.DecimalField(max_digits=4, decimal_places=2, blank=False, default=0.42)
    # service_call_minimum = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=100.00)
    # service_call_gf_chain = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=125.00)
    # service_call_gf_cable = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=150.00)
    # service_call_gf_tubular = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=200.00)
    # service_call_cuckoo = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=100.00)
    # service_call_other = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=100.00)
    # repair_minimum = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=125.00)
    # repair_gf_chain = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=325.00)
    # repair_gf_cable = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=425.00)
    # repair_gf_tubular = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=625.00)
    # repair_cuckoo_minimum = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=150.00)
    # repair_anniversary_minimum = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=150.00)
    # repair_atmos_minimum = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=200.00)
    # repair_other_minimum = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=200.00)
    # multiple_per_train = models.DecimalField(max_digits=3, decimal_places=2, blank=False, default=0.20)
    # multiple_per_activity = models.DecimalField(max_digits=3, decimal_places=2, blank=False, default=0.20)
    # multiple_per_wind_interval = models.DecimalField(max_digits=3, decimal_places=2, blank=False, default=0.20)
    # multiple_per_gf_extra = models.DecimalField(max_digits=3, decimal_places=2, blank=False, default=0.10)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['id'], name='repairer_id_index'),
    #     ]

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('repairer', args=[str(self.id)])

