# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-10 16:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='nationality',
        ),
    ]
