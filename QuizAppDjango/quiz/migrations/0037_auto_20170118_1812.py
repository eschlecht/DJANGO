# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-18 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0036_auto_20170117_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lobby',
            name='current_question',
        ),
        migrations.AddField(
            model_name='userinlobby',
            name='current_question',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ergebnis',
            name='quiz',
            field=models.IntegerField(),
        ),
    ]
