# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-17 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0032_auto_20170112_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='quiz_title',
            field=models.CharField(max_length=200),
        ),
    ]
