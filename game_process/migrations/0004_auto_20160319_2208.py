# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 22:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_process', '0003_auto_20160314_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='modifiedTime',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 19, 22, 8, 2, 501000)),
        ),
        migrations.AlterField(
            model_name='userwaitforinitroom',
            name='wait_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 19, 22, 8, 2, 511000)),
        ),
    ]
