# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-15 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0033_merge_20170115_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiplayerErgebnis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.CharField(max_length=200)),
                ('points', models.IntegerField()),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='quiz',
            name='quiz_title',
            field=models.CharField(max_length=200),
        ),
    ]
