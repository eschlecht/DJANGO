# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20161224_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrank',
            name='total_score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
