# Generated by Django 3.2.8 on 2021-11-20 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Interface', '0008_leaderboard_executiontime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaderboard',
            name='executionTime',
        ),
    ]
