# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-12 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0031_auto_20170112_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ergebnis',
            name='quiz',
            field=models.CharField(max_length=200),
        ),
    ]
