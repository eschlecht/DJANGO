# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-14 09:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0019_auto_20161202_2016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='essayquestion',
            old_name='essay_question_text',
            new_name='question_text',
        ),
        migrations.RenameField(
            model_name='multiplechoicequestion',
            old_name='multi_question_text',
            new_name='question_text',
        ),
        migrations.RenameField(
            model_name='singlechoicequestion',
            old_name='single_question_text',
            new_name='question_text',
        ),
        migrations.RenameField(
            model_name='tfquestion',
            old_name='tf_question_text',
            new_name='question_text',
        ),
    ]