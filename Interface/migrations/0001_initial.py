# Generated by Django 3.2.8 on 2021-11-01 11:16

import Interface.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('categories', models.CharField(choices=[('7-8', 'Class 7 to 8'), ('9-10', 'Class 9 to 10'), ('11-12', 'Class 11 to 12')], max_length=100)),
                ('TimeOfEvent', models.DateTimeField(verbose_name='Date and Time of Event only in UTC (IST not supported for server)')),
                ('timeLimit', models.IntegerField(verbose_name='Time Limit (hrs only)')),
            ],
        ),
        migrations.CreateModel(
            name='Problems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('timeLimit', models.IntegerField()),
                ('problemHtml', models.FileField(default='', upload_to=Interface.models.Problems.upload_path, verbose_name='Problem statement in png')),
                ('mainFile', models.FileField(default='', upload_to=Interface.models.Problems.upload_path, verbose_name='Problem main execution file')),
                ('userFile', models.FileField(default='', upload_to=Interface.models.Problems.upload_path, verbose_name='User execution code file')),
                ('test_module', models.FileField(default='', upload_to=Interface.models.Problems.upload_path, verbose_name='Test cases file (txt)')),
                ('expected_output', models.FileField(default='', upload_to=Interface.models.Problems.upload_path, verbose_name='Expected Answer (txt)')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prob_event', to='Interface.event')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemsSolved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solved', models.BooleanField(default=False, verbose_name='Has Solved')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problem_solved', to='Interface.problems')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solved_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
