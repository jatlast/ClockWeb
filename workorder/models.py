import uuid
from datetime import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from djmoney.models.fields import MoneyField
from repairer.models import Repairer
from clock.models import Clock

class Workorder(models.Model):
    REPAIR_TYPE_CHOICES = [
        ('Service Call','Service/House Call'),
        ('Regulate','Regulate Time'),
        ('Replace Parts','Add/Replace Parts'),
        ('New Movement','Replace Battery Movement'),
        ('Get Working','Adjust/Get Working'),
        ('Clean & Overhaul','Clean & Overhaul'),
    ]

    REPAIR_STATUS_CHOICES = [
        ('Submitted','Submitted for Approval'),
        ('Approved','Approved by Repairer'),
        ('Declined','Declined by Repairer'),
        ('Canceled','Canceled by Customer'),
        ('Scheduled Pickup','Pickup is Scheduled'),
        ('Retrieved','Picked Up by Repairer'),
        ('Started','Started'),
        ('Finished','Finished'),
        ('Scheduled Delivery','Delivery is Scheduled'),
        ('Delivered','Delivered by Repairer'),
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

    # clock_fk - Foreigh Key pointing to the Clock to be serviced
    clock_fk = models.ForeignKey(Clock, on_delete=models.DO_NOTHING)#, default=0)

    # repairer_fk - Freign Key pointing to the Repairer who is being asked to do the work
    repairer_fk = models.ForeignKey(Repairer, on_delete=models.DO_NOTHING)#, default=0)
    # repairer_hourly_rate - attached to workorder in case the repairer changes hourly_rate
    repairer_hourly_rate = MoneyField(max_digits=6, decimal_places=2, blank=False, null=False, default=0.00, default_currency='USD')

    date_created = models.DateTimeField(default=datetime.now, editable=False)

    # General Work Order information fields...
    repair_type = models.CharField(blank=False, max_length=32, choices=REPAIR_TYPE_CHOICES)
    repair_status = models.CharField(blank=False, max_length=32, choices=REPAIR_STATUS_CHOICES, default='Submitted')
    repair_description = models.TextField(blank=False)

    distance_from_repairer = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=0.00)
    # dynamic_estimate - keep original estimate the Customer probably saw before submitting Workorder
    dynamic_estimate = MoneyField(max_digits=6, decimal_places=2, blank=False, null=False, default=0.00, default_currency='USD')
#    repairer_estimate = MoneyField(max_digits=6, decimal_places=2, blank=False, null=False, default=0.00, default_currency='USD')

    # Express estimates in hours instead of currency just as is done when dynamically estimating
    #   The current thought is hours are more universal than any currencies.
    dynamic_estimate_hours = models.DecimalField(max_digits=4, decimal_places=2, blank=False, default=0.00)
    repairer_estimate_hours = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=0.00)

    # Allow the Repairer to accept or decline the work order request.
    repairer_accepted = models.BooleanField(blank=True, default=False)
    repairer_declined = models.BooleanField(blank=True, default=False)

    start_date = models.DateTimeField(blank=True, null=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)

    # total_cost - estimate + additions so the Workorder contains the final total
    total_cost = MoneyField(max_digits=6, decimal_places=2, blank=True, null=False, default=0.00, default_currency='USD')

    def __str__(self):
#        return self.id
        return "%s" % (self.id)
#        return "%s %s" % (self.clock_type, self.footprint)

    def get_absolute_url(self):
        return reverse('workorders', args=[str(self.id)])


class Addons(models.Model):
    ADDON_TYPE_CHOICES = [
        ('Comment','Comment'),
        ('Update','Update'),
        ('Add Parts','Add Parts'),
        ('Add Work','Add Work'),
        ('Request','Request'),
        ('Reply','Reply'),
        ('Approve','Approve Request'),
        ('Refuse','Refuse Request'),
        ('',''),
    ]

    _CHOICES = [
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
    ]

    # id = autopopulated by django

    # workorder_fk - Foreigh Key pointing to the Workorder that is being added to
    workorder_fk = models.ForeignKey(Workorder, on_delete=models.DO_NOTHING)#, default=0)

    date_created = models.DateTimeField(default=datetime.now, editable=False)

    addon_type = models.CharField(blank=False, max_length=32, choices=ADDON_TYPE_CHOICES)

    repair_status_update = models.CharField(blank=False, max_length=32, choices=Workorder.REPAIR_STATUS_CHOICES, default='Submitted')

    addon_description = models.TextField(blank=False)

    added_hours = models.DecimalField(max_digits=3, decimal_places=2, blank=False, default=0.00)
    added_part_cost = MoneyField(max_digits=6, decimal_places=2, blank=False, null=False, default=0.00, default_currency='USD')
    override_part_cost_multiple = models.BooleanField(blank=True, default=False)

    # image_# - Five associated pictures
    image_1 = models.ImageField(upload_to='pics/', blank=True)
    image_2 = models.ImageField(upload_to='pics/', blank=True)
    image_3 = models.ImageField(upload_to='pics/', blank=True)
    image_4 = models.ImageField(upload_to='pics/', blank=True)
    image_5 = models.ImageField(upload_to='pics/', blank=True)
