# Generated by Django 2.1.3 on 2018-12-12 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20181212_0008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citypreference',
            name='user_account',
        ),
    ]
