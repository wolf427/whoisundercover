# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-12 21:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhraseEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstPhrase', models.CharField(max_length=10)),
                ('secondPhrase', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userCount', models.IntegerField()),
                ('modifiedTime', models.DateTimeField()),
                ('phrase_entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game_process.PhraseEntry')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomNum', models.IntegerField()),
                ('userCount', models.IntegerField()),
                ('identityDistribution', models.CharField(max_length=10, null=True)),
                ('modifiedTime', models.DateTimeField(default=datetime.datetime(2016, 3, 12, 21, 52, 39, 143000))),
            ],
        ),
        migrations.CreateModel(
            name='RoomPhraseRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_process.PhraseEntry')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_process.Room')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserInRoomIdentity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity', models.CharField(max_length=10)),
                ('number', models.IntegerField()),
                ('aliveOrDead', models.IntegerField(null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_process.Room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_process.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserWaitForInitRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wait_type', models.CharField(max_length=20)),
                ('wait_time', models.DateTimeField(default=datetime.datetime(2016, 3, 12, 21, 52, 39, 147000))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_process.User')),
            ],
        ),
    ]
