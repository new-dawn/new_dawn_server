# Generated by Django 2.1.3 on 2019-06-25 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_profile_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='city_preference',
            field=models.ManyToManyField(blank=True, to='locations.CityPreference'),
        ),
    ]
