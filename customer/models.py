import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
#from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

class Customer(models.Model):
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
        , editable = False
#        , default=new_uuid
        , default=1
    )
    date_created = models.DateTimeField(default=datetime.now, editable = False)
    first_name = models.CharField(blank=False, max_length=16)
    last_name = models.CharField(blank=False, max_length=16)
#    phone_number = PhoneField(blank=False, help_text='Contact phone number')
    phone_number = PhoneNumberField(blank=False)
    address_street = models.CharField(blank=False, max_length=32)
    address_other = models.CharField(blank=True, max_length=16)
    city = models.CharField(blank=False, max_length=32)
    state = models.CharField(blank=False, max_length=2)
    zipcode = models.CharField(blank=False, max_length=32)

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='customer_id_index'),
        ]
        # permissions = [
        #     ('can_see_all_customers', 'Can see customer list')
        # ]

    # def __str__(self):
    #     return self.id
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
#        return reverse('customer', kwargs={'pk': self.pk})
        return reverse('customer', args=[str(self.id)])

