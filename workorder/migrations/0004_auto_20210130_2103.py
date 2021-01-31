# Generated by Django 3.1.5 on 2021-01-31 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0003_auto_20210130_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addons',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('Cash', 'Cash'), ('Cashier Check', "Cashier's Check"), ('Check', 'Check'), ('Credit Card', 'Credit Card'), ('Direct Deposit', 'Direct Deposit'), ('Electronic Payment', 'Electronic Payment'), ('Money Order', 'Money Order')], max_length=18, null=True),
        ),
    ]
