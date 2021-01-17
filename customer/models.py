import uuid
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from person.models import Person

class Customer(models.Model):
    # UUID for this table
    id = models.UUIDField(
        primary_key = True
        , default = uuid.uuid4
        , editable = False
    )

    # person_fk - Foreigh Key pointing to the Person app
    person_fk = models.ForeignKey(Person, on_delete=models.CASCADE,)

    date_created = models.DateTimeField(default=datetime.now, editable=False)
    company_name = models.CharField(blank=True, max_length=64)

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['id'], name='customer_id_index'),
    #     ]
    #     permissions = [
    #         ('can_see_all_customers', 'Can see customer list')
    #     ]

    def __str__(self):
        return "%s" % (self.id)

    def get_absolute_url(self):
        return reverse('customer', args=[str(self.id)])

