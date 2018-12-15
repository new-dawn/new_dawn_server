# Generated by Django 2.1.3 on 2018-12-12 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20181211_2357'),
        ('locations', '0002_auto_20181211_2357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citypreference',
            name='user_account',
        ),
        migrations.AddField(
            model_name='citypreference',
            name='user_account',
            field=models.ManyToManyField(to='users.Account'),
        ),
    ]