# Generated by Django 2.1.3 on 2018-12-16 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20181212_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='user_defined',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
