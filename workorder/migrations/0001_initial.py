# Generated by Django 3.1.5 on 2021-01-21 20:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repairer', '0001_initial'),
        ('address', '0001_initial'),
        ('customer', '0001_initial'),
        ('clock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workorder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('repairer_hourly_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('repairer_hourly_rate_currency', models.CharField(default='USD', max_length=3)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('date_last_updated', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('repair_type', models.CharField(choices=[('Service Call', 'Service/House Call'), ('Regulate', 'Regulate Time'), ('Replace Parts', 'Add/Replace Parts'), ('New Movement', 'Replace Battery Movement'), ('Get Working', 'Adjust/Get Working'), ('Clean & Overhaul', 'Clean & Overhaul')], help_text="Note: 'Clean & Overhaul' refers to the complete restoration of the clock's mechanical mechanism", max_length=32)),
                ('repair_status', models.CharField(choices=[('Submitted', 'Submitted for Approval'), ('Approved', 'Approved by Repairer'), ('Canceled', 'Canceled by Customer'), ('Declined', 'Declined by Repairer'), ('Scheduled Pickup', 'Pickup is Scheduled'), ('Retrieved', 'Picked Up by Repairer'), ('Started Repair', 'Started Repair'), ('Finished Repair', 'Finished Repair'), ('Timing Out', 'Adjusting Time Accuracy'), ('Scheduled Delivery', 'Delivery is Scheduled'), ('Delivered', 'Delivered by Repairer'), ('Paid in Full', 'Paid in Full')], default='Submitted', max_length=32)),
                ('repair_description', models.TextField(help_text='Describe what is wrong with your clock and what you hope the repair person can do to help')),
                ('distance_from_repairer', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('dynamic_estimate', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('dynamic_estimate_hours', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('total_cost', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6)),
                ('address_clock_fk', models.ForeignKey(help_text='Address where the clock resides', on_delete=django.db.models.deletion.CASCADE, related_name='address_clock', to='address.address')),
                ('address_deliver_fk', models.ForeignKey(blank=True, help_text='Address where the clock is to be deilivered (Note: May be the same as the pick up address', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address_deliver', to='address.address')),
                ('clock_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clock.clock')),
                ('customer_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('repairer_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repairer.repairer')),
            ],
        ),
        migrations.CreateModel(
            name='Addons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('addon_type', models.CharField(choices=[('Comment', 'Comment'), ('Update', 'Update'), ('Add Parts', 'Add Parts'), ('Add Work', 'Add Work'), ('Request', 'Request'), ('Reply', 'Reply'), ('Approve', 'Approve Request'), ('Refuse', 'Refuse Request'), ('', '')], max_length=32)),
                ('repair_status_previous', models.CharField(choices=[('Submitted', 'Submitted for Approval'), ('Approved', 'Approved by Repairer'), ('Canceled', 'Canceled by Customer'), ('Declined', 'Declined by Repairer'), ('Scheduled Pickup', 'Pickup is Scheduled'), ('Retrieved', 'Picked Up by Repairer'), ('Started Repair', 'Started Repair'), ('Finished Repair', 'Finished Repair'), ('Timing Out', 'Adjusting Time Accuracy'), ('Scheduled Delivery', 'Delivery is Scheduled'), ('Delivered', 'Delivered by Repairer'), ('Paid in Full', 'Paid in Full')], default='Submitted', editable=False, max_length=32)),
                ('repair_status_update', models.CharField(choices=[('Submitted', 'Submitted for Approval'), ('Approved', 'Approved by Repairer'), ('Canceled', 'Canceled by Customer'), ('Declined', 'Declined by Repairer'), ('Scheduled Pickup', 'Pickup is Scheduled'), ('Retrieved', 'Picked Up by Repairer'), ('Started Repair', 'Started Repair'), ('Finished Repair', 'Finished Repair'), ('Timing Out', 'Adjusting Time Accuracy'), ('Scheduled Delivery', 'Delivery is Scheduled'), ('Delivered', 'Delivered by Repairer'), ('Paid in Full', 'Paid in Full')], default='Submitted', max_length=32)),
                ('addon_description', models.TextField()),
                ('added_hours', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True)),
                ('added_part_cost', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True)),
                ('part_cost_multiple', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True)),
                ('added_customer_cost', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True)),
                ('image_1', models.ImageField(blank=True, upload_to='workorders/addons/')),
                ('image_2', models.ImageField(blank=True, upload_to='workorders/addons/')),
                ('image_3', models.ImageField(blank=True, upload_to='workorders/addons/')),
                ('image_4', models.ImageField(blank=True, upload_to='workorders/addons/')),
                ('image_5', models.ImageField(blank=True, upload_to='workorders/addons/')),
                ('user_fk', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workorder_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorder.workorder')),
            ],
        ),
    ]
