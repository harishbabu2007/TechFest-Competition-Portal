# Generated by Django 3.2.8 on 2021-11-17 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Interface', '0004_leaderboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='timeLimit',
            field=models.FloatField(default=0.0, verbose_name='Time Limit (hrs only)'),
        ),
    ]
