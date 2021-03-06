# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20161116_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_title', models.CharField(max_length=50)),
                ('semester', models.IntegerField()),
                ('dozent', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='quiz',
            name='coursefk',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='quiz.Course'),
            preserve_default=False,
        ),
    ]
