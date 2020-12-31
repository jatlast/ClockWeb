#import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from datetime import datetime
from customer.models import Customer
from clocktype.models import Clocktype

class Clock(models.Model):
    # id = autopopulated by django
#    id = models.AutoField(primary_key=True, default=1000)

    # user_fk - ID from login credentials
    user_fk = models.ForeignKey(
        get_user_model()
        , on_delete = models.CASCADE
        , editable = False
        , default=1
    )

    # customer - Each Customer can have many clocks but each Clock has only one Customer
#    new_uuid = str(uuid.uuid4())
#    customer_fk = models.ForeignKey(Customer, on_delete=models.CASCADE, default=new_uuid)
    # clocktype - Refers to Clocktype for pre-population but the Customer can change the values
    #   Thus, if the customer changes the values of the Clock it no longer "is" equal to its original Clocktype
    clock_type_fk = models.ForeignKey(Clocktype, on_delete=models.DO_NOTHING, default=3)
    # date_created - autopopulated
    date_created = models.DateTimeField(default=datetime.now, editable=False)
    # clock_type - Advertising, Atmos, Banjo, Kitchen, etc
    #   When displaying use: https://www.antiqueclockspriceguide.com/clocktyperesults.php?t=clocktype.clock_type
    #              Based on: https://www.antiqueclockspriceguide.com/clocktyperesults.php?t=advertising
#    clock_type = models.CharField(blank=False, max_length=32, choices=Clocktype.CLOCK_TYPE_CHOICES, default='Longcase/Grandfather')
    # footprint - Wall, Mantel, Floor
    footprint = models.CharField(blank=False, max_length=16, choices=Clocktype.FOOTPRINT_CHOICES, default='Floor')
    # train_count - NULL,1,2,3,4
    train_count = models.PositiveSmallIntegerField(blank=True, choices=Clocktype.TRAIN_COUNT_CHOICES, default=3)
    # wind_interval_days - NULL, 1, 8, 15, 31
    wind_interval_days = models.PositiveSmallIntegerField(blank=True, choices=Clocktype.WIND_INTERVAL_CHOICES, default=8)
    # drive_type - Mainspring, Chain, Cable, String, Atmospheric, Electric, Battery?
    drive_type = models.CharField(blank=False, max_length=16, choices=Clocktype.DRIVE_TYPE_CHOICES, default='Cable')
    # gear_material - Brass, Wood, Plastic, etc
    gear_material = models.CharField(blank=False, max_length=16, choices=Clocktype.GEAR_MATERIAL_CHOICES, default='Metal')
    # chime_count - 0, 1, 2, 3, 4, ?
    chime_count = models.PositiveSmallIntegerField(blank=False, choices=Clocktype.CHIME_COUNT_CHOICES, default=3)
    # strike_type - Ships Bell, Bim-Bam, Hourly Note, Hourly Chord
    strike_type = models.CharField(blank=False, max_length=32, choices=Clocktype.STRIKE_TYPE_CHOICES, default='Chord')
    # has_pendulum - Yes/No | 1/0
    has_pendulum = models.BooleanField(blank=False, default=False)
    # has_self_adjusting_beat - Yes/No | 1/0
    has_self_adjusting_beat = models.BooleanField(blank=False, default=False)
    # has_self_adjusting_strike - Yes/No | 1/0
    has_self_adjusting_strike = models.BooleanField(blank=False, default=False)
    # has_second_hand - Yes/No | 1/0
    has_second_hand = models.BooleanField(blank=False, default=False)
    # has_off_at_night - Yes/No | 1/0
    has_off_at_night = models.BooleanField(blank=False, default=False)
    # has_calendar - Yes/No | 1/0
    has_calendar = models.BooleanField(blank=False, default=False)
    # has_moon_dial - Yes/No | 1/0
    has_moon_dial = models.BooleanField(blank=False, default=False)
    # has_alarm - Yes/No | 1/0
    has_alarm = models.BooleanField(blank=False, default=False)
    # has_music_box - Yes/No | 1/0
    has_music_box = models.BooleanField(blank=False, default=False)
    # has_activity_other - Yes/No | 1/0 > such as dancing people, wood choppers, water wheel, etc
    has_activity_other = models.BooleanField(blank=False, default=False)
    # has_tubes - Yes/No | 1/0
    has_tubes = models.BooleanField(blank=False, default=False)
    # tube_count - NULL, 5, 9, ?
    tube_count = models.PositiveSmallIntegerField(blank=True, choices=Clocktype.TUBE_COUNT_CHOICES, default=0)
    # choices_are_locked - Yes/No | 1/0 (Customer can only change pictures when True)
    choices_are_locked = models.BooleanField(blank=False, default=False)
    # image_# - Five associated pictures
    image_1 = models.ImageField(upload_to='clock_pics/', blank=True)
    image_2 = models.ImageField(upload_to='clock_pics/', blank=True)
    image_3 = models.ImageField(upload_to='clock_pics/', blank=True)
    image_4 = models.ImageField(upload_to='clock_pics/', blank=True)
    image_5 = models.ImageField(upload_to='clock_pics/', blank=True)


    class Meta:
        indexes = [
            models.Index(fields=['id'], name='clock_id_index'),
        ]
    #     permissions = [
    #         ('can_see_all_customers', 'Can see customer list')
    #     ]

    def __str__(self):
        return "%s %s" % (self.clock_type_fk, self.footprint)

    def get_absolute_url(self):
        return reverse('clock', args=[str(self.id)])


# Tell Django to disreguard previous migrations then re-migrate...
# General
#   docker-compose exec web python manage.py migrate <app_label> zero
# Specific for this project
#   docker-compose exec web python manage.py migrate clock zero

# To show existing migrations
#   django-admin show-migrations

# #### Postgresql #####
# Access postgresql db:
# Example
#   docker exec -it postgres-container psql -U postgres
# Specific for this project
#   docker exec -it books_db_1 psql -U postgres
# List tables
#   \dt
# List Databases
#   SELECT datname FROM pg_database;
# View table schema
#   SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name = 'clock_clock';



