# Generated by Django 2.1.3 on 2018-12-12 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_account_city_preference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='answer_questions',
        ),
    ]
