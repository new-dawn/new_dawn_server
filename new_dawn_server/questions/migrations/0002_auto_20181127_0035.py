# Generated by Django 2.1.1 on 2018-11-27 05:35

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Questions',
            new_name='Question',
        ),
    ]
