# Generated by Django 3.1.5 on 2021-01-24 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clocktypes',
            name='clock_type',
            field=models.CharField(choices=[('Advertising', 'Advertising'), ('Animated', 'Animated'), ('Anniversary', 'Anniversary'), ('Atmos', 'Atmos'), ('Balloon', 'Balloon'), ('Banjo', 'Banjo'), ('Beehive', 'Beehive'), ('Black Mantel', 'Black Mantel'), ('Blinking Eye', 'Blinking Eye'), ('Calendar', 'Calendar'), ('Carriage', 'Carriage'), ('China/Porcelain', 'China/Porcelain'), ('Column', 'Column'), ('Crystal Regulator', 'Crystal Regulator'), ('Cuckoo', 'Cuckoo'), ('Desk', 'Desk'), ('Dial', 'Dial'), ('Drop Trunk/Schoolhouse', 'Drop Trunk/Schoolhouse'), ('Figural', 'Figural'), ('Garnitures', 'Garnitures'), ('Gothic', 'Gothic'), ('Kitchen', 'Kitchen'), ('Lantern', 'Lantern'), ('Longcase/Grandfather', 'Longcase/Grandfather'), ('Lyre', 'Lyre'), ('Mantel', 'Mantel/Shelf'), ('Mission', 'Mission'), ('Mystery', 'Mystery'), ('Ogee', 'Ogee'), ('Picture', 'Picture'), ('Portico', 'Portico'), ('Pillar & Scroll', 'Pillar & Scroll'), ('Plato', 'Plato'), ("Ship's", "Ship's"), ('Skeleton', 'Skeleton'), ('Steeple', 'Steeple'), ('Swinging', 'Swinging'), ('Tambour', 'Tambour'), ('Tape', 'Tape'), ('Vienna Regulator', 'Vienna Regulator'), ('Wag on the Wall', 'Wag on the Wall'), ('Wall', 'Wall')], default='Mantel', max_length=32),
        ),
    ]
