from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
#from django.db import models
from django.urls import reverse
#from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

class Address(models.Model):
    # ADDRESS_TYPE_CHOICES = [
    #     ('Primary','Primary'),
    #     ('Billing','Billing'),
    #     ('Pickup','Pickup'),
    #     ('Delivery','Delivery'),
    #     ('Other','Other'),
    # ]

    # id = autopopulated by django

    # user_fk - ID from login credentials
    user_fk = models.ForeignKey(
        get_user_model()
        , on_delete = models.CASCADE
        , default=1
    )

    date_created = models.DateTimeField(default=datetime.now, editable=False)

    # nickname
    nickname = models.CharField(blank=False, max_length=64)

    # address_type = models.CharField(blank=False, max_length=16, choices=ADDRESS_TYPE_CHOICES)

    contact_name = models.CharField(blank=False, max_length=128)

#    contact_phone = PhoneField(blank=False)
    contact_phone = PhoneNumberField(blank=False)

    ##### Address Specific Fields #####
    address = models.CharField(blank=False, max_length=64)
    address_other = models.CharField(blank=True, max_length=16)

    # Names derived from Mapbox GeoJSON object
    locality_disctrict = models.CharField(blank=True, max_length=64)
    place_city = models.CharField(blank=False, max_length=64)
    
    district_prefectures = models.CharField(blank=True, max_length=64)

    region_state = models.CharField(blank=True, max_length=64)
    postcode = models.CharField(blank=True, max_length=12)
    country = models.CharField(blank=False, max_length=64)
    ###################################

    latitude = models.FloatField(default=42.95)
    longitude = models.FloatField(default=-83.64)
    location = models.PointField(blank=False, default=Point(0.0, 0.0))

    relevance = models.FloatField(blank=True, default=0)
    accuracy = models.CharField(blank=True, max_length=16)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['id'], name='customer_id_index'),
    #     ]
    #     permissions = [
    #         ('can_see_all_customers', 'Can see customer list')
    #     ]

    def __str__(self):
        return "%s" % (str(self.id))
#        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('address', args=[str(self.id)])

