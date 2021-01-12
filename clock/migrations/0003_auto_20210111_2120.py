# Generated by Django 3.1.5 on 2021-01-12 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clock', '0002_auto_20210111_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clocktypes',
            name='clock_type',
            field=models.CharField(choices=[('Advertising-Quartz', 'Advertising-Quartz'), ('Advertising-Electric', 'Advertising-Electric'), ('Advertising-Mechanical', 'Advertising-Mechanical'), ('Animated', 'Animated'), ('Anniversary-Quartz', 'Anniversary-Quartz'), ('Anniversary-Mechanical', 'Anniversary-Mechanical'), ('Atmos', 'Atmos'), ('Balloon', 'Balloon'), ('Banjo', 'Banjo'), ('Beehive', 'Beehive'), ('Black Mantel', 'Black Mantel'), ('Blinking Eye-Quartz', 'Blinking Eye-Quartz'), ('Blinking Eye-Mechanical', 'Blinking Eye-Mechanical'), ('Calendar', 'Calendar'), ('Carriage', 'Carriage'), ('China/Porcelain', 'China/Porcelain'), ('Column', 'Column'), ('Crystal Regulator', 'Crystal Regulator'), ('Cuckoo', 'Cuckoo'), ('Dial-Quartz', 'Dial-Quartz'), ('Dial-Mechanical', 'Dial-Mechanical'), ('School House-Quartz', 'School House-Quartz'), ('School House-Electric', 'School House-Electric'), ('School House-Mechanical', 'School House-Mechanical'), ('Figural', 'Figural'), ('Garnitures', 'Garnitures'), ('Gothic', 'Gothic'), ('Kitchen', 'Kitchen'), ('Lantern', 'Lantern'), ('Grandfather/Grandmother', 'Grandfather/Grandmother'), ('Grandfather/Grandmother-Chains', 'Grandfather/Grandmother-Chains'), ('Grandfather/Grandmother-Cables', 'Grandfather/Grandmother-Cables'), ('Grandfather/Grandmother-Tubular', 'Grandfather/Grandmother-Tubular'), ('Lyre', 'Lyre'), ('Mission', 'Mission'), ('Mystery', 'Mystery'), ('Novelty-Quartz', 'Novelty-Quartz'), ('Novelty-Electric', 'Novelty-Electric'), ('Novelty-Mechanical', 'Novelty-Mechanical'), ('Ogee', 'Ogee'), ('Picture-Quartz', 'Picture-Quartz'), ('Picture-Electric', 'Picture-Electric'), ('Picture-Mechanical', 'Picture-Mechanical'), ('Portico', 'Portico'), ('Pillar & Scroll', 'Pillar & Scroll'), ('Plato', 'Plato'), ('Shelf-Quartz', 'Shelf-Quartz'), ('Shelf-Electric', 'Shelf-Electric'), ('Shelf-Mechanical', 'Shelf-Mechanical'), ("Ship's", "Ship's"), ('Skeleton', 'Skeleton'), ('Steeple', 'Steeple'), ('Swinging', 'Swinging'), ('Tambour', 'Tambour'), ('Tape', 'Tape'), ('Vienna Regulator', 'Vienna Regulator'), ('Wag on the Wall', 'Wag on the Wall'), ('Wall-Quartz', 'Wall-Quartz'), ('Wall-Electric', 'Wall-Electric'), ('Wall-Mechanical', 'Wall-Mechanical')], default='Longcase/Grandfather', max_length=32),
        ),
    ]