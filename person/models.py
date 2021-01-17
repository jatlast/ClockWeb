import uuid
from django.contrib.auth import get_user_model
#from django.contrib.gis.db import models
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

class Person(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('Customer','Customer'),
        ('Repairer','Repair Person'),
    ]

    # id = autopopulated by django

#    user_fk - ID from login credentials
    user_fk = models.ForeignKey(
        get_user_model()
        , on_delete = models.CASCADE
        , default=1
    )

    date_created = models.DateTimeField(default=datetime.now, editable=False)
    first_name = models.CharField(blank=False, max_length=16)
    last_name = models.CharField(blank=False, max_length=16)
    phone = PhoneNumberField(blank=False)
    account_type = models.CharField(blank=False, max_length=8, choices=ACCOUNT_TYPE_CHOICES, default='Customer')

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('person', args=[str(self.id)])

