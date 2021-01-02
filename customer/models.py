import uuid
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
#from django.db import models
from django.urls import reverse
#from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

class Customer(models.Model):
    US_STATE_CHOICES = [
            ('AL', 'Alabama'),
            ('AK', 'Alaska'),
            ('AZ', 'Arizona'),
            ('AR', 'Arkansas'),
            ('CA', 'California'),
            ('CO', 'Colorado'),
            ('CT', 'Connecticut'),
            ('DE', 'Delaware'),
            ('FL', 'Florida'),
            ('GA', 'Georgia'),
            ('HI', 'Hawaii'),
            ('ID', 'Idaho'),
            ('IL', 'Illinois'),
            ('IN', 'Indiana'),
            ('IA', 'Iowa'),
            ('KS', 'Kansas'),
            ('KY', 'Kentucky'),
            ('LA', 'Louisiana'),
            ('ME', 'Maine'),
            ('MD', 'Maryland'),
            ('MA', 'Massachusetts'),
            ('MI', 'Michigan'),
            ('MN', 'Minnesota'),
            ('MS', 'Mississippi'),
            ('MO', 'Missouri'),
            ('MT', 'Montana'),
            ('NE', 'Nebraska'),
            ('NV', 'Nevada'),
            ('NH', 'New Hampshire'),
            ('NJ', 'New Jersey'),
            ('NM', 'New Mexico'),
            ('NY', 'New York'),
            ('NC', 'North Carolina'),
            ('ND', 'North Dakota'),
            ('OH', 'Ohio'),
            ('OK', 'Oklahoma'),
            ('OR', 'Oregon'),
            ('PA', 'Pennsylvania'),
            ('RI', 'Rhode Island'),
            ('SC', 'South Carolina'),
            ('SD', 'South Dakota'),
            ('TN', 'Tennessee'),
            ('TX', 'Texas'),
            ('UT', 'Utah'),
            ('VT', 'Vermont'),
            ('VA', 'Virginia'),
            ('WA', 'Washington'),
            ('WV', 'West Virginia'),
            ('WI', 'Wisconsin'),
            ('WY', 'Wyoming'),
    ]

    # UUID for this table
    id = models.UUIDField(
        primary_key = True
        , default = uuid.uuid4
        , editable = False
    )
    # user_fk - ID from login credentials
#    new_uuid = str(uuid.uuid4()) # Should never be used after everything is working correctly.
    user_fk = models.ForeignKey(
        get_user_model()
        , on_delete = models.CASCADE
#        , editable = False
#        , default=new_uuid
        , default=1
    )
    date_created = models.DateTimeField(default=datetime.now, editable=False)
    first_name = models.CharField(blank=False, max_length=16)
    last_name = models.CharField(blank=False, max_length=16)
#    phone_number = PhoneField(blank=False)
    phone_number = PhoneNumberField(blank=False)
    address_street = models.CharField(blank=False, max_length=32)
    address_other = models.CharField(blank=True, max_length=16)
    city = models.CharField(blank=False, max_length=32)
    state = models.CharField(blank=False, max_length=2, choices=US_STATE_CHOICES)
    zipcode = models.CharField(blank=False, max_length=32)

    latitude = models.FloatField(default=42.95)
    longitude = models.FloatField(default=-83.64)
    location = models.PointField(blank=False, default=Point(0.0, 0.0))

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['id'], name='customer_id_index'),
    #     ]
    #     permissions = [
    #         ('can_see_all_customers', 'Can see customer list')
    #     ]

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('customer', args=[str(self.id)])

