# Generated by Django 3.1.5 on 2021-01-25 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairer', '0002_auto_20210125_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairer',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
