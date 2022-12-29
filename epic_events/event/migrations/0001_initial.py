# Generated by Django 4.1.4 on 2022-12-29 21:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Coming', 'Coming'), ('Ended', 'Ended')], max_length=12)),
                ('notes', models.TextField(blank=True, max_length=500)),
                ('attendees', models.PositiveIntegerField(default=1)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 12, 29, 21, 19, 12, 648388))),
            ],
        ),
    ]
