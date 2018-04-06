# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-06 22:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('faculty_planner', '0002_auto_20180406_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDateGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Course Date',
                'verbose_name_plural': 'Course Dates',
            },
        ),
        migrations.RemoveField(
            model_name='course',
            name='location',
        ),
        migrations.RemoveField(
            model_name='coursedate',
            name='group',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='specialization_group',
        ),
        migrations.AddField(
            model_name='professor',
            name='link',
            field=models.TextField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='schedule',
            name='course_dates',
            field=models.ManyToManyField(through='faculty_planner.ScheduleCourseDate', to='faculty_planner.CourseDate'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Specialization'),
        ),
        migrations.AlterField(
            model_name='coursedate',
            name='end_hour',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='coursedate',
            name='start_hour',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='professor',
            name='email',
            field=models.CharField(default='', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='coursedategroup',
            name='course_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.CourseDate'),
        ),
        migrations.AddField(
            model_name='coursedategroup',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Group'),
        ),
        migrations.AddField(
            model_name='coursedate',
            name='groups',
            field=models.ManyToManyField(through='faculty_planner.CourseDateGroup', to='faculty_planner.Group'),
        ),
    ]
