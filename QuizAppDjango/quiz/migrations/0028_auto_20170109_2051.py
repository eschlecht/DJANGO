# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-09 19:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0027_auto_20170109_2047'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EssayQuestionPropose',
            new_name='ProposeEssayQuestion',
        ),
        migrations.RenameModel(
            old_name='MultipleChoiceQuestionPropose',
            new_name='ProposeMultipleChoiceQuestion',
        ),
        migrations.RenameModel(
            old_name='SingleChoiceQuestionPropose',
            new_name='ProposeSingleChoiceQuestion',
        ),
        migrations.RenameModel(
            old_name='TFQuestionPropose',
            new_name='ProposeTFQuestion',
        ),
    ]