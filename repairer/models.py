import uuid
from djmoney.models.fields import MoneyField
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from person.models import Person

class Repairer(models.Model):
    # UUID for this table
    id = models.UUIDField(
        primary_key = True
        , default = uuid.uuid4
        , editable = False
    )

    # person_fk - Foreigh Key pointing to the Person app
    person_fk = models.ForeignKey(Person, on_delete=models.CASCADE,)

    # General contact information fields...
    date_created = models.DateTimeField(default=datetime.now, editable=False)
    company_name = models.CharField(blank=True, max_length=64)

    experience_in_years = models.PositiveSmallIntegerField(blank=False, default=1, help_text='Enter total years of experience')
    still_accepting_jobs = models.BooleanField(blank=False, default=True, help_text='Select if you are still accepting new Work Orders')
    makes_service_calls = models.BooleanField(blank=False, default=False, help_text='Select if you are willing to do remote location, on-site service calls')
    service_call_hours_minimum = models.PositiveSmallIntegerField(blank=False, default=2, help_text='This number is multiplied by hourly rate to determine the minimum servie charge')
    repairs_grandfathers = models.BooleanField(blank=False, default=False, help_text='Select if you work on Longcase / Grandfather clocks')
    repairs_tubular_grandfathers = models.BooleanField(blank=False, default=False, help_text='Select if you work on Tubular Chime - Longcase / Grandfather clocks')
    repairs_cuckoos = models.BooleanField(blank=False, default=False, help_text='Select if you work on Cuckoo clocks')
    repairs_atmospherics = models.BooleanField(blank=False, default=False, help_text='Select if you work on Atmos clocks')
    repairs_anniversarys = models.BooleanField(blank=False, default=False, help_text='Select if you work on 400 Day / Anniversary clocks')
    repairs_most_mechanical = models.BooleanField(blank=False, default=False, help_text='Select if you work on mechanical clocks')
    repairs_most_quartz = models.BooleanField(blank=False, default=False, help_text='Select if you work on quartz clocks')

    # Fields to dynamically determine pricing...
    hourly_rate = MoneyField(max_digits=6, decimal_places=2, blank=False, null=False, default=25.00, default_currency='USD', help_text='Hourly Rate is used to dynamically estimate clock repairs.  This site automatically determines the hours required for different repairs and uses the total hours required * hourly rate = dynamic estimate')
#    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=25.00)
    road_time_minutes_included = models.PositiveSmallIntegerField(blank=False, default=15, help_text='This is the "rount trip" road time included')
    road_time_minutes_maximum = models.PositiveSmallIntegerField(blank=False, default=120, help_text='The maximum round trip road time you are willing to travel')

    personal_description = models.TextField(blank=False, default='Tell potential customers about yourself...', help_text="Whatever you type here will be seen by potential Customers on the Repairer's About page")
    # image_# - Five associated pictures
    image_1 = models.ImageField(upload_to='repairers/', blank=True, height_field="This picture will be seen by potential Customers on the Repairer's About page")
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

