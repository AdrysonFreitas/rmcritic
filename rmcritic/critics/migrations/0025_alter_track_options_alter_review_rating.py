# Generated by Django 4.1.3 on 2022-11-30 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('critics', '0024_remove_album_get_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='track',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
