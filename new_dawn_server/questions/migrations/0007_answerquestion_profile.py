# Generated by Django 2.1.3 on 2018-12-12 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20181212_0905'),
        ('questions', '0006_remove_answerquestion_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerquestion',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Profile'),
        ),
    ]
