# Generated by Django 3.1.5 on 2021-01-07 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clock', '0002_auto_20210106_2157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clock',
            old_name='dial_diameter_millimeters',
            new_name='dial_diameter_centimeters',
        ),
        migrations.AlterField(
            model_name='clock',
            name='strike_type',
            field=models.CharField(choices=[('None', 'No Strike'), ('Bim-Bam', 'Bim-Bam'), ('Cuckoo', 'Cuckoo'), ('Note', 'Hourly Note'), ('Chord', 'Hourly Chord')], default='Chord', max_length=32),
        ),
    ]
