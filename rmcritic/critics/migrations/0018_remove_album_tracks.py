# Generated by Django 4.1.3 on 2022-11-16 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('critics', '0017_track_parent_artist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='tracks',
        ),
    ]
