# Generated by Django 2.1.3 on 2019-04-06 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_auto_20190405_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerquestion',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Profile'),
        ),
    ]
