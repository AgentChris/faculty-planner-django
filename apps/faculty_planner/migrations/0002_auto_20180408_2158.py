# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-08 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty_planner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedate',
            name='end_hour',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='coursedate',
            name='start_hour',
            field=models.TimeField(null=True),
        ),
    ]
