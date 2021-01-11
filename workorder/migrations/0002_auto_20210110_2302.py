# Generated by Django 3.1.5 on 2021-01-11 04:02

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='distance_from_repairer',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='dynamic_estimate_hours',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='repairer_estimate_hours',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='total_cost',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('0.0'), default_currency='USD', max_digits=6),
        ),
    ]
