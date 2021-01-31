import uuid
from datetime import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
#from django.contrib.gis.db import models
from django.db import models
# from djmoney.models.fields import MoneyField
from repairer.models import Repairer
from clock.models import Clock
from customer.models import Customer
from address.models import Address

class Workorder(models.Model):
    REPAIR_TYPE_CHOICES = [
        ('House Call','House Call'),
        # Same as Clean & Overhaul
        ('Refurbish Mechanical','Clean / Overhaul Mechanical Clock'),
        ('Refurbish Quartz','Refurbish / Replace Battery Movement'),
        # Same as Clean & Overhaul
        ('Refurbish Electric','Refurbish / Replace Electric Movement'),
        ('Get Working','Adjust / Get Working'),
        ('Replace Parts','Add / Replace Parts'),
        ('Mechanical to Quartz','Replace Mechanical Movement w/ Battery Movement'),
        ('Regulate','Regulate Time'),
        ('Prepair to Move','Prepair Grandfather Clock for Move / Shipping'),
        ('Move Grandfather','Move Grandfather Clock fron one Address to Another'),
    ]

    REPAIR_STATUS_CHOICES = [
        ('Submitted','Submitted for Approval'),
        ('Approved','Approved by Repairer'),
        ('Canceled','Canceled by Customer'),
        ('Declined','Declined by Repairer'),
        ('Scheduled Pickup','Pickup is Scheduled'),
        ('Scheduled House Call','House Call is Scheduled'),
        ('Retrieved','Picked Up by Repairer'),
        ('Started Repair','Started Repair'),
        ('Finished Repair','Finished Repair'),
        ('Timing Out','Adjusting Time Accuracy'),
        ('Scheduled Delivery','Delivery is Scheduled'),
        ('Delivered','Delivered by Repairer'),
        ('Paid in Full','Paid in Full'),
        ('Partial Payment','Partial Payment'),
    ]

    # UUID for this table
    id = models.UUIDField(
        primary_key = True
        , default = uuid.uuid4
        , editable = False
    )

    # customer_fk - Foreigh Key pointing to the Customer that is adding this Workorder
    customer_fk = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # clock_fk - Foreigh Key pointing to the Clock to be serviced
    clock_fk = models.ForeignKey(Clock, on_delete=models.CASCADE)#, default=0)

    # repairer_fk - Freign Key pointing to the Repairer who is being asked to do the work
    repairer_fk = models.ForeignKey(Repairer, on_delete=models.CASCADE)#, default=0)

    # address_deliver - Foreigh Key pointing to the Address app
    address_clock_fk = models.ForeignKey(Address, related_name='address_clock', on_delete=models.CASCADE, blank=False, null=False, help_text='Address where the clock resides')
    address_deliver_fk = models.ForeignKey(Address, related_name='address_deliver', on_delete=models.CASCADE, blank=True, null=True, help_text='Address where the clock is to be deilivered (Note: May be the same as the pick up address')

    # repairer_hourly_rate - attached to workorder in case the repairer changes hourly_rate
    repairer_hourly_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=0.00)
    repairer_hourly_rate_currency = models.CharField(max_length=3, blank=False, default='USD')
    # repairer_hourly_rate = MoneyField(max_digits=6, decimal_places=2, blank=False, null=False, default=0.00, default_currency='USD')

    date_created = models.DateTimeField(default=datetime.now, editable=False)
    date_last_updated = models.DateTimeField(default=datetime.now, editable=False)

    # General Work Order information fields...
    repair_type = models.CharField(blank=False, max_length=32, choices=REPAIR_TYPE_CHOICES, help_text="Note: 'Clean & Overhaul' refers to the complete restoration of the clock's mechanical mechanism")
    repair_status = models.CharField(blank=False, max_length=32, choices=REPAIR_STATUS_CHOICES, default='Submitted')
    repair_description = models.TextField(blank=False, help_text='Describe what is wrong with your clock and what you hope the repair person can do to help')

    distance_from_repairer = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=0.00)
    # dynamic_estimate - keep original estimate the Customer probably saw before submitting Workorder
    dynamic_estimate = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.00)
#    dynamic_estimate = MoneyField(max_digits=6, decimal_places=2, blank=False, null=False, default=0.00, default_currency='USD')
#    repairer_estimate = MoneyField(max_digits=6, decimal_places=2, blank=False, null=False, default=0.00, default_currency='USD')

    # Express estimates in hours instead of currency just as is done when dynamically estimating
    #   The current thought is hours are more universal than any currencies.
    dynamic_estimate_hours = models.DecimalField(max_digits=4, decimal_places=2, blank=False, default=0.00)
    # repairer_estimate_hours = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=0.00)

    # Allow the Repairer to accept or decline the work order request.
    # repairer_accepted = models.BooleanField(blank=True, default=False)
    # repairer_declined = models.BooleanField(blank=True, default=False)

    # start_date = models.DateTimeField(blank=True, null=True)
    # finish_date = models.DateTimeField(blank=True, null=True)
    # date_paid = models.DateTimeField(blank=True, null=True)

    # total_cost - estimate + additions so the Workorder contains the final total
    total_cost = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0.00)
#    total_cost = MoneyField(max_digits=6, decimal_places=2, blank=True, null=False, default=0.00, default_currency='USD')

    def __str__(self):
#        return self.id
        return "%s" % (self.id)
#        return "%s %s" % (self.clock_type, self.footprint)

    def get_absolute_url(self):
        return reverse('workorder', args=[str(self.id)])

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
        ('Payment','Payment'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash','Cash'),
        ('Cashier Check',"Cashier's Check"),
        ('Credit Card','Credit Card'),
        ('Direct Deposit','Direct Deposit'),
        ('Electronic Payment','Electronic Payment'),
        ('Money Order','Money Order'),
    ]

    # id = autopopulated by django

    # workorder_fk - Foreigh Key pointing to the Workorder that is being added to
    workorder_fk = models.ForeignKey(Workorder, on_delete=models.CASCADE)#, default=0)

    # user_fk - ID from login credentials
    user_fk = models.ForeignKey(
        get_user_model()
        , on_delete = models.CASCADE
#        , editable = False
        , default=1
    )

    date_created = models.DateTimeField(default=datetime.now, editable=False)
#    added_by = models.CharField(blank=False, max_length=8, choices=ADDED_BY_CHOICES, default='Repairer')

    addon_type = models.CharField(blank=False, max_length=32, choices=ADDON_TYPE_CHOICES)

    repair_status_previous = models.CharField(blank=False, max_length=32, editable=False, choices=Workorder.REPAIR_STATUS_CHOICES, default='Submitted')
    repair_status_update = models.CharField(blank=False, max_length=32, choices=Workorder.REPAIR_STATUS_CHOICES, default='Submitted')

    addon_description = models.TextField(blank=False)

    added_hours = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=0.00)
    # added_part_cost = MoneyField(max_digits=6, decimal_places=2, blank=True, null=True, default=0.00, default_currency='USD')
    added_part_cost = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=0.00)
    part_cost_multiple = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, default=0.00)
    added_customer_cost = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=0.00)

    payment_method = models.CharField(blank=True, null=True, max_length=18, choices=PAYMENT_METHOD_CHOICES)
    payment_information = models.CharField(blank=True, null=True, max_length=32)
    payment_amount = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2, default=0)

    # image_# - Five associated pictures
    image_1 = models.ImageField(upload_to='workorders/addons/', blank=True)
    image_2 = models.ImageField(upload_to='workorders/addons/', blank=True)
    image_3 = models.ImageField(upload_to='workorders/addons/', blank=True)
    image_4 = models.ImageField(upload_to='workorders/addons/', blank=True)
    image_5 = models.ImageField(upload_to='workorders/addons/', blank=True)
