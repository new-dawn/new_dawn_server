# Generated by Django 2.1.1 on 2018-11-26 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
        ('users', '0005_auto_20181119_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='answer_questions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='questions.AnswerQuestions'),
        ),
    ]