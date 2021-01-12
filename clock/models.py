#import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from datetime import datetime
#from customer.models import Customer
#from clocktype.models import Clocktype

class Clocktypes(models.Model):
    CLOCK_TYPE_CHOICES=[
        ('Advertising-Quartz', 'Advertising-Quartz'),
        ('Advertising-Electric', 'Advertising-Electric'),
        ('Advertising-Mechanical', 'Advertising-Mechanical'),
        ('Animated', 'Animated'),
        ('Anniversary-Quartz', 'Anniversary-Quartz'),
        ('Anniversary-Mechanical', 'Anniversary-Mechanical'),
        ('Atmos', 'Atmos'),
        ('Balloon', 'Balloon'),
        ('Banjo', 'Banjo'),
        ('Beehive', 'Beehive'),
        ('Black Mantel', 'Black Mantel'),
        ('Blinking Eye-Quartz', 'Blinking Eye-Quartz'),
        ('Blinking Eye-Mechanical', 'Blinking Eye-Mechanical'),
        ('Calendar', 'Calendar'),
        ('Carriage', 'Carriage'),
        ('China/Porcelain', 'China/Porcelain'),
        ('Column', 'Column'),
        ('Crystal Regulator', 'Crystal Regulator'),
        ('Cuckoo', 'Cuckoo'),
        ('Dial-Quartz', 'Dial-Quartz'),
        ('Dial-Mechanical', 'Dial-Mechanical'),
        ('School House-Quartz', 'School House-Quartz'),
        ('School House-Electric', 'School House-Electric'),
        ('School House-Mechanical', 'School House-Mechanical'),
        ('Figural', 'Figural'),
        ('Garnitures', 'Garnitures'),
        ('Gothic', 'Gothic'),
        ('Kitchen', 'Kitchen'),
        ('Lantern', 'Lantern'),
        ('Grandfather/Grandmother', 'Grandfather/Grandmother'),
        ('Grandfather/Grandmother-Chains', 'Grandfather/Grandmother-Chains'),
        ('Grandfather/Grandmother-Cables', 'Grandfather/Grandmother-Cables'),
        ('Grandfather/Grandmother-Tubular', 'Grandfather/Grandmother-Tubular'),
        ('Lyre', 'Lyre'),
        ('Mission', 'Mission'),
        ('Mystery', 'Mystery'),
        ('Novelty-Quartz', 'Novelty-Quartz'),
        ('Novelty-Electric', 'Novelty-Electric'),
        ('Novelty-Mechanical', 'Novelty-Mechanical'),
        ('Ogee', 'Ogee'),
        ('Picture-Quartz', 'Picture-Quartz'),
        ('Picture-Electric', 'Picture-Electric'),
        ('Picture-Mechanical', 'Picture-Mechanical'),
        ('Portico', 'Portico'),
        ('Pillar & Scroll', 'Pillar & Scroll'),
        ('Plato', 'Plato'),
        ('Shelf-Quartz', 'Shelf-Quartz'),
        ('Shelf-Electric', 'Shelf-Electric'),
        ('Shelf-Mechanical', 'Shelf-Mechanical'),
        ("Ship's", "Ship's"),
        ('Skeleton', 'Skeleton'),
        ('Steeple', 'Steeple'),
        ('Swinging', 'Swinging'),
        ('Tambour', 'Tambour'),
        ('Tape', 'Tape'),
        ('Vienna Regulator', 'Vienna Regulator'),
        ('Wag on the Wall', 'Wag on the Wall'),
        ('Wall-Quartz', 'Wall-Quartz'),
        ('Wall-Electric', 'Wall-Electric'),
        ('Wall-Mechanical', 'Wall-Mechanical'),
    ]

    FOOTPRINT_CHOICES = [
        ('Desktop','Desktop'),
        ('Floor','Floor'),
        ('Mantle','Mantle'),
        ('Wall','Wall'),
    ]

    TRAIN_COUNT_CHOICES = [
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    ]

    WIND_INTERVAL_CHOICES = [
        (0,'Never - Quartz/Battery/Electric/Atmos'),
        (1,'Once Every Day'),
        (8,'Once Every Week'),
        (15,'Once Every Other Week'),
        (31,'Once Every Month'),
        (400,'Once Every Year'),
    ]

    DRIVE_TYPE_CHOICES = [
        ('Mainspring','Mainspring - Wind Up'),
        ('Chain','Weights on Chains'),
        ('Cable','Weights on Cable with Pullies'),
        ('String','Weights on String'),
        ('Atmospheric','Atmospheric'),
        ('Electric','Electric'),
        ('Quartz','Battery/Quartz'),
    ]

    GEAR_MATERIAL_CHOICES = [
        ('Metal','Metal Gears'),
        ('Wood','Wooden Gears'),
        ('Plastic','Plastic Gears'),
    ]

    CHIME_COUNT_CHOICES = [
        (0,'No Chime'),
        (1,'Single Chime'),
        (2,'Dual Chime'),
        (3,'Triple Chime'),
        (4,'4+ Chime Options'),
    ]

    STRIKE_TYPE_CHOICES = [
        ('None','No Strike'),
        ('Bim-Bam','Bim-Bam'),
        ('Cuckoo','Cuckoo'),
        ('Chord','Hourly Chord'),
        ('Note','Hourly Note'),
        ('Ship',"Ship's Bells"),
    ]

    BATTERY_COUNT_CHOICES = [
        (0,'0'),
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5+'),
    ]

    TUBE_COUNT_CHOICES = [
        (0,'Zero'),
        (5,'Five Tubes'),
        (9,'Nine Tubes'),
    ]

    _CHOICES = [
        ('',''),
        ('',''),
        ('',''),
        ('',''),
        ('',''),
    ]

    # id = autopopulated by django
#    id = models.AutoField(primary_key=True, default=0)

    # date_created - autopopulated
    date_created = models.DateTimeField(default=datetime.now, editable = False)
    # clock_type - Advertising, Atmos, Banjo, Kitchen, etc
    #   When displaying use: https://www.antiqueclockspriceguide.com/clocktyperesults.php?t=clocktype.clock_type
    #              Based on: https://www.antiqueclockspriceguide.com/clocktyperesults.php?t=advertising
    clock_type = models.CharField(blank=False, max_length=32, choices=CLOCK_TYPE_CHOICES, default='Longcase/Grandfather')
    # footprint - Wall, Mantel, Floor
    footprint = models.CharField(blank=False, max_length=16, choices=FOOTPRINT_CHOICES, default='Floor')
    # dial_diameter_centimeters - NULL or integer
    dial_diameter_centimeters = models.PositiveSmallIntegerField(blank=True, default=0)
    # has_glass_over_face - Yes/No | 1/0
    has_glass_over_face = models.BooleanField(blank=False, default=False)
    # train_count - NULL,1,2,3,4
    train_count = models.PositiveSmallIntegerField(blank=True, choices=TRAIN_COUNT_CHOICES, default=3)
    # wind_interval_days - NULL, 1, 8, 15, 31
    wind_interval_days = models.PositiveSmallIntegerField(blank=True, choices=WIND_INTERVAL_CHOICES, default=8)
    # drive_type - Mainspring, Chain, Cable, String, Atmospheric, Electric, Battery?
    drive_type = models.CharField(blank=False, max_length=16, choices=DRIVE_TYPE_CHOICES, default='Cable')
    # gear_material - Brass, Wood, Plastic, etc
    gear_material = models.CharField(blank=False, max_length=16, choices=GEAR_MATERIAL_CHOICES, default='Metal')
    # chime_count - 0, 1, 2, 3, 4, ?
    chime_count = models.PositiveSmallIntegerField(blank=False, choices=CHIME_COUNT_CHOICES, default=3)
    # strike_type - Ships Bell, Bim-Bam, Hourly Note, Hourly Chord
    strike_type = models.CharField(blank=False, max_length=32, choices=STRIKE_TYPE_CHOICES, default='Chord')
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
    # has_light - Yes/No | 1/0
    has_light = models.BooleanField(blank=False, default=False)
    # battery_count - NULL, 5, 9, ?
    battery_count = models.PositiveSmallIntegerField(blank=True, choices=BATTERY_COUNT_CHOICES, default=0)
    # has_tubes - Yes/No | 1/0
    has_tubes = models.BooleanField(blank=False, default=False)
    # tube_count - NULL, 5, 9, ?
    tube_count = models.PositiveSmallIntegerField(blank=True, choices=TUBE_COUNT_CHOICES, default=0)
    # choices_are_locked - Yes/No | 1/0 (Customer can only change pictures when True)
    choices_are_locked = models.BooleanField(blank=False, default=False)
    # image_# - Five associated pictures
    image_1 = models.ImageField(upload_to='clocks/types/', blank=True)
    image_2 = models.ImageField(upload_to='clocks/types/', blank=True)
    image_3 = models.ImageField(upload_to='clocks/types/', blank=True)
    image_4 = models.ImageField(upload_to='clocks/types/', blank=True)
    image_5 = models.ImageField(upload_to='clocks/types/', blank=True)


#     class Meta:
#         indexes = [
#             models.Index(fields=['id'], name='clocktype_id_index'),
#         ]
#         # permissions = [
#         #     ('can_see_all_customers', 'Can see customer list')
#         # ]

    def __str__(self):
        return self.clock_type
#        return "%s %s" % (self.clock_type, self.footprint)

#     def get_absolute_url(self):
#         return reverse('detail', args=[str(self.id)])

class Clock(models.Model):
    # id = autopopulated by django
#    id = models.AutoField(primary_key=True, default=1000)

    # user_fk - ID from login credentials
    user_fk = models.ForeignKey(
        get_user_model()
        , on_delete = models.CASCADE
#        , editable = False
        , default=1
    )

    # nickname - Wall, Mantel, Floor
    nickname = models.CharField(blank=False, max_length=32, default='Nickname', help_text='Please choose a Nickname to identify this clock')
    # customer - Each Customer can have many clocks but each Clock has only one Customer
#    new_uuid = str(uuid.uuid4())
#    customer_fk = models.ForeignKey(Customer, on_delete=models.CASCADE, default=new_uuid)
    # clocktype - Refers to Clocktype for pre-population but the Customer can change the values
    #   Thus, if the customer changes the values of the Clock it no longer "is" equal to its original Clocktype
    clock_type_fk = models.ForeignKey(Clocktypes, on_delete=models.DO_NOTHING, default=1)
    # date_created - autopopulated
    date_created = models.DateTimeField(default=datetime.now, editable=False)
    # clock_type - Advertising, Atmos, Banjo, Kitchen, etc
    #   When displaying use: https://www.antiqueclockspriceguide.com/clocktyperesults.php?t=clocktype.clock_type
    #              Based on: https://www.antiqueclockspriceguide.com/clocktyperesults.php?t=advertising
#    clock_type = models.CharField(blank=False, max_length=32, choices=Clocktype.CLOCK_TYPE_CHOICES, default='Longcase/Grandfather')
    # footprint - Wall, Mantel, Floor
    footprint = models.CharField(blank=False, max_length=16, choices=Clocktypes.FOOTPRINT_CHOICES, default='Floor')
    # dial_diameter_centimeters - NULL or integer
    dial_diameter_centimeters = models.PositiveSmallIntegerField(blank=True, default=0, help_text='(Note: Dial diameter is only import for large battery operated clocks)')
    # has_glass_over_face - Yes/No | 1/0
    has_glass_over_face = models.BooleanField(blank=False, default=False, help_text='(Note: Has glass over face is only import for large battery operated clocks)')
    # train_count - NULL,1,2,3,4
    train_count = models.PositiveSmallIntegerField(blank=True, help_text='How many places the clock winds (i.e., if you wind it in two place your clock has a train count of 2)', choices=Clocktypes.TRAIN_COUNT_CHOICES, default=3)
    # wind_interval_days - NULL, 1, 8, 15, 31
    wind_interval_days = models.PositiveSmallIntegerField(blank=True, choices=Clocktypes.WIND_INTERVAL_CHOICES, default=8, help_text='How often do you have to wind this clock?')
    # drive_type - Mainspring, Chain, Cable, String, Atmospheric, Electric, Battery?
    drive_type = models.CharField(blank=False, max_length=16, choices=Clocktypes.DRIVE_TYPE_CHOICES, default='Cable', help_text='Drive type is what powers the clock')
    # gear_material - Brass, Wood, Plastic, etc
    gear_material = models.CharField(blank=False, max_length=16, choices=Clocktypes.GEAR_MATERIAL_CHOICES, default='Metal', help_text='For battery clocks choose "Plastic" for most others choos "Metal"')
    # chime_count - 0, 1, 2, 3, 4, ?
    chime_count = models.PositiveSmallIntegerField(blank=False, choices=Clocktypes.CHIME_COUNT_CHOICES, default=3, help_text='(Note: Chimes usually ring every quarter) | Chime count indicates how many different chime options your clock has. Some have none, others only Westminster, and some Grandfather clocks have, say: Westminster, Whittenauer, and Saint Michael; battery/quartz clocks can have 3-4+ chime optons')
    # strike_type - Ships Bell, Bim-Bam, Hourly Note, Hourly Chord
    strike_type = models.CharField(blank=False, max_length=32, choices=Clocktypes.STRIKE_TYPE_CHOICES, default='Chord', help_text='(Note: Strike is hourly) | If the clock hammer strikes a coil/bell/rod then it is a "Note," if two or more rods it is a "Chord"')
    # has_pendulum - Yes/No | 1/0
    has_pendulum = models.BooleanField(blank=False, default=False, help_text='Select if your clock has a Pendulum')
    # has_self_adjusting_beat - Yes/No | 1/0
    has_self_adjusting_beat = models.BooleanField(blank=False, default=False, help_text='Leave this field as is.  The Repairer will understand and set it correctly')
    # has_self_adjusting_strike - Yes/No | 1/0
    has_self_adjusting_strike = models.BooleanField(blank=False, default=False, help_text='Leave this field as is.  The Repairer will understand and set it correctly')
    # has_second_hand - Yes/No | 1/0
    has_second_hand = models.BooleanField(blank=False, default=False, help_text='Select if your clock has a second hand')
    # has_off_at_night - Yes/No | 1/0
    has_off_at_night = models.BooleanField(blank=False, default=False, help_text='If you are unsure, leave this field as is.  The Repairer will understand and set it correctly')
    # has_calendar - Yes/No | 1/0
    has_calendar = models.BooleanField(blank=False, default=False, help_text='If you are unsure, leave this field as is.  The Repairer will understand and set it correctly')
    # has_moon_dial - Yes/No | 1/0
    has_moon_dial = models.BooleanField(blank=False, default=False, help_text='If you are unsure, leave this field as is.  The Repairer will understand and set it correctly')
    # has_alarm - Yes/No | 1/0
    has_alarm = models.BooleanField(blank=False, default=False, help_text='Select if your clock has an alarm feature. (Mostly for quartz/battery, Kitchen clocks, and Alarm clocks)')
    # has_music_box - Yes/No | 1/0
    has_music_box = models.BooleanField(blank=False, default=False, help_text='Select if your Cuckoo clock has a music box')
    # has_activity_other - Yes/No | 1/0 > such as dancing people, wood choppers, water wheel, etc
    has_activity_other = models.BooleanField(blank=False, default=False, help_text='Select if your Cuckoo clock has features such as dancing wheel and/or any other moving features on its face')
    # has_light - Yes/No | 1/0
    has_light = models.BooleanField(blank=False, default=False, help_text='Select if your clock has a light')
    # battery_count - NULL, 5, 9, ?
    battery_count = models.PositiveSmallIntegerField(blank=True, choices=Clocktypes.BATTERY_COUNT_CHOICES, default=0, help_text='How many batteries does your clock take?')
    # has_tubes - Yes/No | 1/0
    has_tubes = models.BooleanField(blank=False, default=False, help_text='Only Tubular Grandfather clocks have this rare and expensive feature.  Such clocks have 5 to 9 tubes that hang down nearly the full height of the clock.  The are usually about 10 to 15 centimiters in diameter.')
    # tube_count - NULL, 5, 9, ?
    tube_count = models.PositiveSmallIntegerField(blank=True, choices=Clocktypes.TUBE_COUNT_CHOICES, default=0, help_text='If your clock "Has tubes" then count them and enter the total number of Tubes here.')
    # choices_are_locked - Yes/No | 1/0 (Customer can only change their clock information when True)
    choices_are_locked = models.BooleanField(blank=False, default=False, help_text='(Note: Customer can only change their clock information when True)')
    # image_# - Five associated pictures
    image_1 = models.ImageField(upload_to='clocks/', blank=True, help_text='Please add at least one picture of this clock')
    image_2 = models.ImageField(upload_to='clocks/', blank=True)
    image_3 = models.ImageField(upload_to='clocks/', blank=True)
    image_4 = models.ImageField(upload_to='clocks/', blank=True)
    image_5 = models.ImageField(upload_to='clocks/', blank=True)


    class Meta:
        indexes = [
            models.Index(fields=['id'], name='clock_id_index'),
        ]
    #     permissions = [
    #         ('can_see_all_customers', 'Can see customer list')
    #     ]

    def __str__(self):
#        return self.clock_type_fk
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
#   docker exec -it books_db_1 psql -h localhost -U docker gis
# List tables
#   \dt
# List Databases
#   SELECT datname FROM pg_database;
# View table schema
#   SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name = 'clock_clock';

# Reset the image url from 'clock_pics/' to 'pics/'
#   select image_1 from clocktype_clocktype  where image_1 like '%pics/%';
#       update clocktype_clocktype set image_1 = replace(image_1, 'pics', 'clocks/types') where image_1 like '%pics/%';
#   select image_1 from clock_clock  where image_1 like '%pics/%';
#       update clock_clock set image_1 = replace(image_1, 'pics', 'clocks') where image_1 like '%pics/%';

# Docker Commands...
#   List volumes:
#       docker volume ls
#   Inspect a volume:
#       docker volume inspect books_postgis-data
