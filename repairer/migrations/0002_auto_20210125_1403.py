# Generated by Django 3.1.5 on 2021-01-25 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairer',
            name='hide_my_address',
            field=models.BooleanField(default=False, help_text='Select to prevent customers from seeing your full address'),
        ),
        migrations.AddField(
            model_name='repairer',
            name='hide_my_email',
            field=models.BooleanField(default=False, help_text='Select to prevent customers from seeing your email address'),
        ),
        migrations.AddField(
            model_name='repairer',
            name='hide_my_phone',
            field=models.BooleanField(default=False, help_text='Select to prevent customers from seeing your telephone number'),
        ),
    ]
