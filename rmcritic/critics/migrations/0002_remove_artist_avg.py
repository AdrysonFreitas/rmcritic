# Generated by Django 4.1.3 on 2022-11-15 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('critics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='avg',
        ),
    ]
