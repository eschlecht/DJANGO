# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-04 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0023_lobby_started'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobby',
            name='current_question',
            field=models.IntegerField(default=0),
        ),
    ]
