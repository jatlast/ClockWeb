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
    phone = PhoneNumberField(blank=False)

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

    personal_description = models.TextField(blank=False, default='Tell potential customers about yourself...')
    # image_# - Five associated pictures
    image_1 = models.ImageField(upload_to='repairers/', blank=True)
    image_2 = models.ImageField(upload_to='repairers/', blank=True)
    image_3 = models.ImageField(upload_to='repairers/', blank=True)
    image_4 = models.ImageField(upload_to='repairers/', blank=True)
    image_5 = models.ImageField(upload_to='repairers/', blank=True)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['id'], name='repairer_id_index'),
    #     ]

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('repairer', args=[str(self.id)])

