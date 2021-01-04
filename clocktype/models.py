from django.db import models
from django.urls import reverse
from datetime import datetime

class Clocktype(models.Model):
    CLOCK_TYPE_CHOICES=[
        ('Advertising', 'Advertising'),
        ('Animated', 'Animated'),
        ('Anniversary', 'Anniversary'),
        ('Atmos', 'Atmos'),
        ('Balloon', 'Balloon'),
        ('Banjo', 'Banjo'),
        ('Beehive', 'Beehive'),
        ('Black Mantel', 'Black Mantel'),
        ('Blinking Eye', 'Blinking Eye'),
        ('Calendar', 'Calendar'),
        ('Carriage', 'Carriage'),
        ('China/Porcelain', 'China/Porcelain'),
        ('Column', 'Column'),
        ('Crystal Regulator', 'Crystal Regulator'),
        ('Cuckoo', 'Cuckoo'),
        ('Dial', 'Dial'),
        ('Drop Trunk/School House', 'Drop Trunk/School House'),
        ('Figural', 'Figural'),
        ('Garnitures', 'Garnitures'),
        ('Gothic', 'Gothic'),
        ('Kitchen', 'Kitchen'),
        ('Lantern', 'Lantern'),
        ('Longcase/Grandfather', 'Longcase/Grandfather'),
        ('Lyre', 'Lyre'),
        ('Mission', 'Mission'),
        ('Mystery', 'Mystery'),
        ('Novelty', 'Novelty'),
        ('Ogee', 'Ogee'),
        ('Picture', 'Picture'),
        ('Portico', 'Portico'),
        ('Pillar & Scroll', 'Pillar & Scroll'),
        ('Plato', 'Plato'),
        ('Shelf', 'Shelf'),
        ("Ship's", "Ship's"),
        ('Skeleton', 'Skeleton'),
        ('Steeple', 'Steeple'),
        ('Swinging', 'Swinging'),
        ('Tambour', 'Tambour'),
        ('Tape', 'Tape'),
        ('Vienna Regulator', 'Vienna Regulator'),
        ('Wag on the Wall', 'Wag on the Wall'),
        ('Wall', 'Wall'),
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
        (0,'Never - Quartz/Battery/Atmos'),
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
        ('Note','Hourly Note'),
        ('Chord','Hourly Chord'),
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
    # dial_diameter_millimeters - NULL or integer
    dial_diameter_millimeters = models.PositiveSmallIntegerField(blank=True, default=0)
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
    image_1 = models.ImageField(upload_to='clock_pics/', blank=True)
    image_2 = models.ImageField(upload_to='clock_pics/', blank=True)
    image_3 = models.ImageField(upload_to='clock_pics/', blank=True)
    image_4 = models.ImageField(upload_to='clock_pics/', blank=True)
    image_5 = models.ImageField(upload_to='clock_pics/', blank=True)


    class Meta:
        indexes = [
            models.Index(fields=['id'], name='clocktype_id_index'),
        ]
        # permissions = [
        #     ('can_see_all_customers', 'Can see customer list')
        # ]

    def __str__(self):
        return self.clock_type
#        return "%s %s" % (self.clock_type, self.footprint)

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])


