# Generated by Django 4.1.3 on 2022-11-16 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('critics', '0012_alter_album_options_alter_review_options_album_year'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='album',
            name='year',
        ),
    ]
